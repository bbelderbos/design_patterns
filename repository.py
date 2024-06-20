from abc import ABC, abstractmethod
from sqlmodel import SQLModel, create_engine, Session, Field, select


class Item(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str


class IRepository(ABC):
    @abstractmethod
    def add(self, item: Item):
        pass

    @abstractmethod
    def get(self, name: str) -> Item | None:
        pass


class SQLModelRepository(IRepository):
    def __init__(self, db_string="sqlite:///todo.db"):
        self.engine = create_engine(db_string)
        SQLModel.metadata.create_all(self.engine)
        self.session = Session(self.engine)

    def add(self, item: Item):
        self.session.add(item)
        self.session.commit()

    def get(self, name: str) -> Item | None:
        statement = select(Item).where(Item.name == name)
        return self.session.exec(statement).first()


class CsvRepository(IRepository):
    def __init__(self, file_path="todo.csv"):
        self._file_path = file_path

    def add(self, item: Item):
        with open(self._file_path, "a") as f:
            f.write(f"{item.id},{item.name}\n")

    def get(self, name: str) -> Item | None:
        with open(self._file_path, "r") as f:
            return next(
                (
                    Item(id=int(id_str), name=item_name)
                    for line in f
                    if (id_str := line.strip().split(",", 1)[0])
                    and (item_name := line.strip().split(",", 1)[1]) == name
                ),
                None,
            )


if __name__ == "__main__":
    repo = SQLModelRepository()
    repo.add(Item(name="Buy Milk"))
    sql_item = repo.get("Buy Milk")

    # Swap out the repository implementation
    csv_repo = CsvRepository()
    csv_repo.add(Item(id=1, name="Buy Milk"))
    csv_item = csv_repo.get("Buy Milk")

    print(f"{sql_item=}, {csv_item=}, {sql_item == csv_item=}")
    # outputs:
    # sql_item=Item(name='Buy Milk', id=1), csv_item=Item(id=1, name='Buy Milk'), sql_item == csv_item=True
