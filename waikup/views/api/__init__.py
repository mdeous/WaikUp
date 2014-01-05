# -*- coding: utf-8 -*-


class Resource(object):
    name = ''
    fields = ()
    fk_map = {}

    def __init__(self, obj):
        self.obj = obj

    @property
    def dict(self):
        result = {}
        for field in self.fields:
            value = getattr(self.obj, field)
            if field in self.fk_map:
                value = getattr(value, self.fk_map[field])
            result[field] = value
        return result

    @property
    def data(self):
        return {"success": True, self.name: self.dict}


class ResourceSet(object):
    def __init__(self, resource_cls, objs):
        self.name = resource_cls.name + 's'
        self.resources = []
        for obj in objs:
            self.resources.append(resource_cls(obj))

    @property
    def data(self):
        result = {"success": True, self.name: []}
        for resource in self.resources:
            result[self.name].append(resource.dict)
        return result
