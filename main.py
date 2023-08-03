from enum import Enum
import logging
import fastapi
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()


class Breed(Enum):
    visla = "visla"
    pitbull = "pitbull"


class Dog(BaseModel):
    name: str = Field(None, max_length=10)
    breed: Breed
    price: float = Field(None, gt=0, lt=100000)




dogs = {}
current_dog_id = 0

logging.basicConfig(level=logging.DEBUG)


@app.get("/")
async def root():
    logging.info(f'Getting all dogs')
    logging.debug(f"dogs {dogs}")
    return {"dogs": dogs}


# get dog as dog id parameter
@app.get("/dogs/{dog_id}")
async def query_item_by_id(dog_id: int) -> Dog:
    logging.info(f'Getting dog with id: {dog_id}')
    if dog_id not in dogs:
        logging.error(f'Dog id {dog_id} not found in db for delete')
        logging.debug(dogs)
        raise fastapi.HTTPException(status_code=404, detail="dog does not exist")
    return dogs[dog_id]

# uvicorn main:app --reload

@app.post("/")
async def create_dog(dog: Dog) -> Dict[str, Dog]:
    logging.info(f'post all dogs')
    global current_dog_id
    current_dog_id += 1
    dogs[current_dog_id] = dog
    return {f"added (dog id) : {len(dogs) - 1}": dog}


@app.delete("/delete/{dog_id}")
def delete_item(dog_id: int) -> Dict[str, Dog]:
    logging.info(f'delete dog id: {dog_id}')
    if dog_id not in dogs:
        logging.error(f'Dog id {dog_id} not found in db')
        logging.debug(dogs)
        raise fastapi.HTTPException(status_code=404, detail="dog does not exist")
    dog=dogs.pop(dog_id)
    return {"deleted dog":dog}


@app.put("/dogs/{dog_id}", response_model=Dog)
async def update_item(dog_id: str, dog: Dog):
    update_item_encoded = jsonable_encoder(dog)
    dogs[dog_id] = update_item_encoded
    if dog_id not in dogs:
        logging.error(f'Dog id {dog_id} not found in db')
        logging.debug(dogs)
    return update_item_encoded






if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)