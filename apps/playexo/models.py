import json
import logging

import jinja2
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from assets.models import Asset
from playactivity.models import Activity
from playcourse.models import Course
from playexo import jinja2_custom
from playexo.components import components_source
from playexo.exceptions import BuildError, GradeError
from playexo.utils import (DEFAULT_BUILDER, DEFAULT_GRADER, async_get_less_used_sandbox,
                           create_seed,
                           tar_from_dic)


logger = logging.getLogger(__name__)



class PL(Asset):
    name = models.CharField(null=False, max_length=100)
    data = models.JSONField(default=dict)
    course = models.ForeignKey(Course, blank=True, null=True, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, blank=True, null=True, on_delete=models.CASCADE)
    demo = models.BooleanField(default=False)
    rerollable = models.BooleanField(default=False)
    compilation_date = models.DateField(default=timezone.now)



class PLSession(models.Model):
    context = models.JSONField(default=dict)
    saved_data = models.JSONField(default=dict)
    pl = models.ForeignKey(PL, null=False, on_delete=models.CASCADE)
    seed = models.IntegerField(null=False)
    try_count = models.IntegerField(default=0)
    
    
    @staticmethod
    def _build_env(pl_data: dict, answer: dict = None) -> dict:
        env = dict(pl_data['__files'])
        env["components.py"] = components_source()
        
        tmp = dict(pl_data)
        del tmp['__files']
        env['pl.json'] = json.dumps(tmp)
        
        if 'grader' in pl_data and 'grader.py' not in env:
            env['grader.py'] = pl_data['grader']
        
        if 'builder' in pl_data and 'builder.py' not in env:
            env['builder.py'] = pl_data['builder']
        
        if answer is not None:
            env['answer.json'] = json.dumps(answer)
        
        return tar_from_dic(env)
    
    
    @classmethod
    async def build_context(cls, pl: PL, seed: int = None, params: dict = None) -> (dict, int):
        pl_data = dict(pl.data)
        if params is not None:
            pl_data = pl_data.update(params)
        sandbox = await async_get_less_used_sandbox()
        
        if seed is None and "seed" not in pl_data:
            pl_data["seed"] = create_seed()
        elif seed is not None:
            pl_data["seed"] = seed
        
        env = cls._build_env(pl_data)
        config = pl_data.get("config", {}).get("builder", DEFAULT_BUILDER)
        if config is not None:
            logger.info("Building on sandbox '" + str(sandbox) + "'.")
            execution = await sandbox.execute(config=config, environment=env)
            
            if not execution.success:
                raise BuildError(execution.traceback)
            else:
                return json.loads(execution.response["result"]), pl_data["seed"]
        return pl_data, pl_data["seed"]
    
    
    def get_view_data(self) -> dict:
        context = dict(self.context)
        jinja_env = jinja2_custom.environment(undefined=jinja2_custom.CustomUndefined)
        jinja_keys = self.context.get("config", {}).get("filters", {}).get("jinja2",
                                                                           ["title", "text",
                                                                            "form"])
        for key in jinja_keys:
            if type(context[key]) is str:
                try:
                    context[key] = jinja_env.from_string(context[key]).render(**self.context)
                except Exception as e:
                    continue
        data = {
            "title":      context["title"],
            "form":       context["form"],
            "text":       context["text"],
            "config":     context.get("config", {}),
            "rerollable": self.pl.rerollable,
            "demo":       self.pl.demo
        }
        if "styles" in context:
            data["styles"] = context["styles"]
        if "scripts" in context:
            data["scripts"] = context["scripts"],
        return data
    
    
    async def evaluate(self, answers: dict):
        pl = await database_sync_to_async(self.__getattribute__)("pl")
        sandbox = await async_get_less_used_sandbox()
        context = {**pl.data, **self.context}
        config = context.get("config", {}).get("grader", DEFAULT_GRADER)
        env = self._build_env(context, answer=answers)
        execution = await sandbox.execute(config=config, environment=env)
        
        if not execution.success:
            raise GradeError(execution.traceback)
        else:
            new_context = json.loads(execution.response["result"])
        try:
            grade = new_context["grade"]
            feedback = new_context["feedback"]
            del new_context["grade"]
            del new_context["feedback"]
        except KeyError as e:
            raise GradeError("grade and feedback must be added to context")
        
        self.context.update(new_context)
        self.try_count += 1
        await database_sync_to_async(self.save)()
        
        return grade, feedback
    
    
    async def reroll(self, seed: int = None, params: dict = None):
        context, seed = await self.build_context(self.pl, seed, params)
        self.context = context
        self.seed = seed
        self.save()
    
    
    def best_answer(self):
        return Answer.objects.all().prefetch_related("session").filter(session=self).order_by(
            "date").order_by("grade")
    
    
    def last_answer(self):
        return Answer.objects.all().prefetch_related("session").filter(session=self).latest()



class LoggedPLSession(PLSession):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    @classmethod
    async def build(cls, pl: PL, user: User, seed: int = None, params: dict = None) -> PLSession:
        context, seed = await super().build_context(pl, seed, params)
        return await database_sync_to_async(cls.objects.create)(context=context, pl=pl, user=user,
                                                                seed=seed)



class AnonPLSession(PLSession):
    user_id = models.UUIDField(null=False)
    
    
    @classmethod
    async def build(cls, pl: PL, user_id: str, seed: int = None, params: dict = None) -> PLSession:
        context, seed = await super().build_context(pl, seed, params)
        return await database_sync_to_async(cls.objects.create)(context=context, pl=pl,
                                                                user_id=user_id,
                                                                seed=seed)



class Answer(models.Model):
    session = models.ForeignKey(PLSession, null=True, on_delete=models.SET_NULL)
    date = models.DateField(default=timezone.now)
    answer = models.JSONField()
    seed = models.IntegerField()
    grade = models.IntegerField(null=False)
