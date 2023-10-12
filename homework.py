class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: int,  # время тренирови
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type};'
                f'Длительность: {self.duration:.3f} ч.;'
                f'Дистанция: {self.distance:.3f} км;'
                f'Ср. скорость: {self.speed:.3f} км/ч;'
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP_W: float = 0.65
    LEN_STEP_SW: float = 1.38
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP_W / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.action * self.LEN_STEP_W / self.M_IN_KM

    def get_spent_calories(self) -> None:
        """Получить количество затраченных калорий."""
        pass  # остается пустым

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    # def __init__(self, action, duration, weight):
    #     super().__init__(action, duration, weight)

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP_W / self.M_IN_KM

    """Расчет калории."""
    def get_spent_calories(self):
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * self.duration * 60)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    Sp_Walk1: float = 0.035
    Sp_Walk2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> float:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.height = height

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP_W / self.M_IN_KM

    """Расчет калорий. """

    def get_spent_calories(self) -> float:
        return ((self.Sp_Walk1 * self.weight
                + ((self.get_mean_speed()) ** 2 / self.height)
                * self.Sp_Walk2 * self.weight)
                * self.duration)


class Swimming(Training):
    """Тренировка: плавание."""

    Sw_1: float = 1.1
    Sw_2: int = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 lenght_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = lenght_pool
        self.count_pool = count_pool

    """Расчет средней скорости."""

    def get_mean_speed(self) -> float:
        return (self.lenght_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    """Расчет калорий."""

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.Sw_1)
                * self.Sw_2 * self.weight
                * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return workout[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    PACKAGE = [('SWM', [720, 1, 80, 25, 40]),
               ('RUN', [15000, 1, 75]),
               ('WLK', [9000, 1, 75, 180]),]


for workout_type, data in PACKAGE:
    training = read_package(workout_type, data)
    main(training)
