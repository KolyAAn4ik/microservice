from pydantic import BaseModel, Field, computed_field, field_validator, model_validator


class User(BaseModel):
    name: str
    surname: str
    age: int
    price: float = Field(gt=0, description='Цена должна быть больше нуля')

    @computed_field
    def full_name(self) -> str:
        return f'{self.name} {self.surname}'
    
    @field_validator('age')
    def check_age(cls, value) -> str:
        if value < 18:
            raise ValueError('персик дозревай')
        return value
    
    @model_validator(mode="after")
    def second_check(self):
        if len(self.name) > 100:
            raise ValueError("недопустимое имя")
        return self
