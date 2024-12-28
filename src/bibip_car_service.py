from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
import shutil
import os


class CarService:
    def __init__(self, root_directory_path: str):
        self.root_directory_path = root_directory_path

    # Create dir if not exist
    def create_directory(self, root_directory_path: str) -> None:
        try:
            os.makedirs(self.root_directory_path)
            print(f"Папка была успешно создана в {self.root_directory_path}")
        except FileExistsError:
            print(f"Дериктория проекта - {self.root_directory_path}")
        except Exception as e:
            print(f"Произошла ошибка при создании папки: {e}")

    # Create directory if not exist
    def create_path(self, root_directory_path: str, name: str) -> str | None:
        source_path = "c:/Dev/de-project-bibip/tables/"
        destination_path = root_directory_path
        path = destination_path + name
        if not os.path.exists(destination_path + name):
            try:
                shutil.copyfile(source_path + name, destination_path + name)
                print(f"Файл {name} скопирован в {destination_path + name}")
                return path
            except Exception as e:
                print(f"Произошла ошибка при копировании файла: {e}")
                return None
        return path

    # get indexes into RAM
    def get_indexes(self, path: str, key_type: str) -> dict:
        index_dict = dict()
        try:
            with open(path, "r") as file:
                for line in file:
                    key, value = line.strip().split("=")
                    if key_type == "str":
                        index_dict[key] = value
                    elif key_type == "int":
                        index_dict[int(key)] = value
                file.close()
        except Exception as e:
            print(f"Произошла ошибка: {e}")

        return index_dict

    # get row number from .txt file with a path
    def get_current_row_number(self, path: str) -> int:
        with open(path, "r") as file:
            content = file.read().strip()
            if content == "":
                row_number = 0
            else:
                row_number = int(content)
            file.close()
        return row_number

    # update indexes in .txt file with a path
    def update_indexes(self, path: str, index_dict: dict) -> None:
        sorted_indexes_list = sorted(index_dict.keys())
        try:
            with open(path, "w") as file:
                file.write("")
                for key in sorted_indexes_list:
                    file.write(f"{key}={index_dict[key]}\n")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    # update row_number in .txt file with a path
    def update_row_number(self, row_number: int, path: str) -> None:
        value = str(row_number)
        with open(path, "w") as file:
            file.write(value)

    # write string to .txt file with a path
    def add_str_to_file(self, value: str, path: str) -> None:
        with open(path, "a+") as file:
            file.write(f"{value}\n")
            file.close()
        return print(value)

    # ljust string to 500 symbols
    def ljust_500(self, value: str) -> str:
        value_500 = value.ljust(500)
        return value_500

    # get row by key
    def get_row_number_by_key(
            self, index_dict: dict, 
            key: str | int) -> None | int:
        try:
            row_number = int(index_dict[key])
            return row_number
        except KeyError:
            print(f"Ключ {key} отсутсвует")
            return None
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return None

    # find row in _____.txt by key using ____ _index.txt
    def get_row_by_key(
            self, path: str, 
            index_dict: dict, 
            key: str | int) -> None | str:
        try:
            row_number = self.get_row_number_by_key(index_dict, key)
            with open(path, "a+") as file:
                file.seek(row_number * (503))
                value = file.read(499)
                file.close()
                return value
        except KeyError:
            print(f"Ключ {key} отсутсвует")
            return None
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return None

    # update_row_by_row_number
    def update_row_by_row_number(
            self, path: str, 
            value: str, 
            row_number: int) -> None:
        with open(path, "r+") as file:
            file.seek(int(row_number) * (503))
            file.write(f"{value}\n")
            file.close()

    # clean line
    def clean_line(self, line: str) -> str:
        clean_line = str(line).strip(" ;\n")
        return clean_line

    # Задание 1. Сохранение автомобилей и моделей
    # add new model
    def add_model(self, model: Model) -> Model:
        # create dir, txt, paths
        self.create_directory(self.root_directory_path)
        models_path = self.create_path(self.root_directory_path, "models.txt")
        models_index_path = self.create_path(
            self.root_directory_path, "models_index.txt"
        )
        models_row_number_path = self.create_path(
            self.root_directory_path, "models_row_number.txt"
        )
        # get indexes
        models_indexes = self.get_indexes(models_index_path, "int")
        # check duplicates
        try:
            id = int(model.id)
            models_indexes[id]
            print(f"Модель {model.brand} {model.name} уже существует в базе!")
            return model
        except KeyError:
            print(f"Модель {model.brand} {model.name} в базе отсутсвует")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return model
        # collect data
        id = model.id
        row_number = self.get_current_row_number(models_row_number_path)
        index = f"{id}={row_number}"
        models_indexes[int(model.id)] = row_number
        try:
            model_500 = self.ljust_500(Car.model_dump_json(model)) + ";"
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return model
        # push to tables
        self.add_str_to_file(model_500, models_path)
        self.add_str_to_file(index, models_index_path)
        self.update_row_number(row_number + 1, models_row_number_path)
        self.update_indexes(models_index_path, models_indexes)
        print(f"Модель {model.brand} {model.name} добавлена в базу!")
        return model

    # add new car
    def add_car(self, car: Car) -> Car:
        # create dir, txt, paths
        self.create_directory(self.root_directory_path)
        cars_path = self.create_path(self.root_directory_path, "cars.txt")
        cars_index_path = self.create_path(
            self.root_directory_path, "cars_index.txt"
            )
        cars_row_number_path = self.create_path(
            self.root_directory_path, "cars_row_number.txt"
        )
        # get indexes
        cars_indexes = self.get_indexes(cars_index_path, "str")
        # check duplicates
        try:
            cars_indexes[car.vin]
            print(f"Машина {car.vin} уже существует в базе!")
            return car
        except KeyError:
            print(f"Машина {car.vin} в базе отсутсвует")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return car
        # prepare data
        vin = car.vin
        row_number = self.get_current_row_number(cars_row_number_path)
        index = f"{vin}={row_number}"
        cars_indexes[car.vin] = row_number
        try:
            car_500 = self.ljust_500(Car.model_dump_json(car)) + ";"
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return car
        # push to tables
        self.add_str_to_file(car_500, cars_path)
        self.add_str_to_file(index, cars_index_path)

        self.update_row_number(row_number + 1, cars_row_number_path)
        self.update_indexes(cars_index_path, cars_indexes)
        print(f"Машина {car.vin} добавлена в базу!")
        return car

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:
        # create dir, txt, paths
        self.create_directory(self.root_directory_path)
        sales_path = self.create_path(self.root_directory_path, "sales.txt")
        sales_index_path = self.create_path(self.root_directory_path, "sales_index.txt")
        sales_row_number_path = self.create_path(
            self.root_directory_path, "sales_row_number.txt"
        )
        cars_path = self.create_path(self.root_directory_path, "cars.txt")
        cars_index_path = self.create_path(self.root_directory_path, "cars_index.txt")
        # get indexes
        sales_indexes = self.get_indexes(sales_index_path, "str")
        cars_indexes = self.get_indexes(cars_index_path, "str")
        # check duplicates
        try:
            sales_indexes[sale.sales_number]
            print(f"Продажа {sale.sales_number} уже существует в базе!")
            return None
        except KeyError:
            print(f"Новая продажа {sale.sales_number}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return None
        # prepare data
        row_number = self.get_current_row_number(sales_row_number_path)
        index = f"{sale.sales_number}={row_number}"
        sales_indexes[sale.sales_number] = row_number
        sale_500 = self.ljust_500(Sale.model_dump_json(sale)) + ";"
        # push to sales's tables
        self.add_str_to_file(sale_500, sales_path)
        self.add_str_to_file(index, sales_index_path)
        self.update_row_number(row_number + 1, sales_row_number_path)
        self.update_indexes(sales_index_path, sales_indexes)
        print(f"Продажа {sale.sales_number} добавлена в базу!")
        # change status in car.txt
        car_str = self.get_row_by_key(cars_path, cars_indexes, sale.car_vin)
        try:
            car = Car.model_validate_json(car_str)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return None
        car.status = CarStatus.sold
        car_row_number = self.get_row_number_by_key(cars_indexes, car.vin)
        sold_car = self.ljust_500(Car.model_dump_json(car)) + ";"
        self.update_row_by_row_number(cars_path, sold_car, car_row_number)
        return car

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        # create dir, txt, paths
        self.create_directory(self.root_directory_path)
        cars_path = self.create_path(self.root_directory_path, "cars.txt")
        car_list = []
        with open(cars_path, "r") as file:
            for line in file:
                clean_line = self.clean_line(line)
                try:
                    car = Car.model_validate_json(clean_line)
                except Exception as e:
                    print(f"Произошла ошибка: {e}")
                    return None
                if car.status == status:  # and car.is_deleted == False:
                    car_list.append(car)
        return car_list

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        # create dir, txt, paths
        self.create_directory(self.root_directory_path)
        cars_path = self.create_path(self.root_directory_path, "cars.txt")
        cars_index_path = self.create_path(self.root_directory_path, "cars_index.txt")
        models_path = self.create_path(self.root_directory_path, "models.txt")
        models_index_path = self.create_path(
            self.root_directory_path, "models_index.txt"
        )
        sales_path = self.create_path(self.root_directory_path, "sales.txt")
        # get indexes
        models_indexes = self.get_indexes(models_index_path, "int")
        cars_indexes = self.get_indexes(cars_index_path, "str")
        # get car
        car_str = self.get_row_by_key(cars_path, cars_indexes, vin)
        try:
            car = Car.model_validate_json(car_str)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return None
        # get model
        model_key = int(car.model)
        model_str = self.get_row_by_key(models_path, models_indexes, model_key)
        try:
            model = Model.model_validate_json(model_str)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return None
        # get sale
        if car.status == "sold":
            with open(sales_path, "r") as file:
                for line in file:
                    clean_line = self.clean_line(line)
                    sale = Sale.model_validate_json(clean_line)
                    if sale.car_vin == vin:
                        sales_date = sale.sales_date
                        sales_cost = sale.cost
                file.close()
        else:
            sales_date = None
            sales_cost = None

        car_full_info = CarFullInfo(
            vin=vin,
            car_model_name=model.name,
            car_model_brand=model.brand,
            price=car.price,
            date_start=car.date_start,
            status=car.status,
            sales_date=sales_date,
            sales_cost=sales_cost,
        )
        return car_full_info

    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:
        # create dir, txt, paths
        self.create_directory(self.root_directory_path)
        cars_path = self.create_path(self.root_directory_path, "cars.txt")
        cars_index_path = self.create_path(self.root_directory_path, "cars_index.txt")
        # get indexes
        cars_indexes = self.get_indexes(cars_index_path, "str")
        # get car
        car_str = self.get_row_by_key(cars_path, cars_indexes, vin)
        car_clean = self.clean_line(car_str)
        try:
            car = Car.model_validate_json(car_clean)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return None
        row_number = self.get_row_number_by_key(cars_indexes, car.vin)
        del cars_indexes[car.vin]
        # update vin
        car.vin = new_vin
        car_str = self.ljust_500(Car.model_dump_json(car)) + ";"
        self.update_row_by_row_number(cars_path, car_str, row_number)
        # update indexes
        cars_indexes[car.vin] = row_number
        self.update_indexes(cars_index_path, cars_indexes)
        return car

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        # create dir, txt, paths
        self.create_directory(self.root_directory_path)
        sales_path = self.create_path(self.root_directory_path, "sales.txt")
        sales_index_path = self.create_path(self.root_directory_path, "sales_index.txt")
        sales_row_number_path = self.create_path(
            self.root_directory_path, "sales_row_number.txt"
        )
        cars_path = self.create_path(self.root_directory_path, "cars.txt")
        cars_index_path = self.create_path(self.root_directory_path, "cars_index.txt")
        # get indexes
        sales_indexes = self.get_indexes(sales_index_path, "str")
        cars_indexes = self.get_indexes(cars_index_path, "str")
        # get sale
        sale_str = self.get_row_by_key(sales_path, sales_indexes, sales_number)
        sale_clean = self.clean_line(sale_str)
        try:
            sale = Sale.model_validate_json(sale_clean)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return None
        sale_row_number = self.get_row_number_by_key(sales_indexes, sales_number)
        # get car
        car_str = self.get_row_by_key(cars_path, cars_indexes, sale.car_vin)
        car_clean = self.clean_line(car_str)
        try:
            car = Car.model_validate_json(car_clean)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            return None
        car_row_number = self.get_row_number_by_key(cars_indexes, car.vin)
        # change status in car.txt
        car.status = CarStatus.available
        avaible_car = self.ljust_500(Car.model_dump_json(car)) + ";"
        self.update_row_by_row_number(cars_path, avaible_car, car_row_number)
        # delete sale
        self.update_row_by_row_number(sales_path, "is_deleted", sale_row_number)
        return car

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        # create dir, txt, paths
        self.create_directory(self.root_directory_path)
        cars_path = self.create_path(self.root_directory_path, "cars.txt")
        cars_index_path = self.create_path(self.root_directory_path, "cars_index.txt")
        models_path = self.create_path(self.root_directory_path, "models.txt")
        models_index_path = self.create_path(
            self.root_directory_path, "models_index.txt"
        )
        sales_path = self.create_path(self.root_directory_path, "sales.txt")
        # get indexes
        models_indexes = self.get_indexes(models_index_path, "int")
        cars_indexes = self.get_indexes(cars_index_path, "str")
        # get sales dict
        sales = dict()
        with open(sales_path, "r") as file:
            for sale in file:
                clean_sale = self.clean_line(sale)
                sale = Sale.model_validate_json(clean_sale)
                car_str = str(
                    self.get_row_by_key(cars_path, cars_indexes, sale.car_vin)
                )
                clean_car = self.clean_line(car_str)
                car = Car.model_validate_json(clean_car)
                model_key = car.model
                sales_number = sales.get(model_key, [0, 0])[0] + 1
                car_price = sales.get(model_key, [0, 0])[1] + car.price
                content = [sales_number, car_price]
                sales[model_key] = content
        top_sales = dict(sorted(sales.items(), key=lambda item: item[1], reverse=True))
        # get top 3
        i = 0
        top_3_list = []
        for key in top_sales:
            if i == 3:
                break
            else:
                model_line = self.get_row_by_key(models_path, models_indexes, key)
                model_json = Model.model_validate_json(model_line)
                car_model_name = model_json.name
                brand = model_json.brand
                sales_number = sales.get(key)[0]
                top_3_list.append(
                    ModelSaleStats(
                        car_model_name=car_model_name,
                        brand=brand,
                        sales_number=sales_number,
                    )
                )
                i += 1
        print(top_3_list)
        return top_3_list
