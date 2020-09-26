from typing import Union, Literal, Set, Dict, Any

from pydantic import create_model, BaseModel


class Clonable(BaseModel):
    @classmethod
    def partial(cls):
        return cls.clone(to_optional='__all__')

    @classmethod
    def clone(
            cls,
            *,
            fields: Set[str] = None,
            exclude: Set[str] = None,
            to_optional: Union[Literal['__all__'], Set[str], Dict[str, Any]] = None
    ) -> 'Clonable':
        if fields is None:
            fields = set(cls.__fields__.keys())

        if exclude is None:
            exclude = set()

        if to_optional == '__all__':
            opt = {f: None for f in fields}
            opt.update(cls.__field_defaults__)
        elif isinstance(to_optional, set):
            opt = {f: None for f in to_optional}
            opt.update(cls.__field_defaults__)
        else:
            opt = cls.__field_defaults__.copy()
            opt.update(to_optional or {})

        model = create_model(
            cls.__name__,
            __base__=Clonable,
            **{
                field: (cls.__annotations__[field], opt.get(field, ...))
                for field in fields - exclude
            }
        )
        model.__name__ += str(id(model))
        return model
