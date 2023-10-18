from typing import Type


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):

        self.training_type: str = training_type
        self.duration: float = duration
        self.distance: float = distance
        self.speed: float = speed
        self.calories: float = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

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
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

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

    def get_spent_calories(self) -> float:
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight / self.M_IN_KM
            * (
                self.duration * self.MIN_IN_H
            )
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALLORIES_SPORT_WALK_1 = 0.035
    CALLORIES_SPORT_WALK_2 = 0.029
    CM_IN_M = 100
    KPH_TO_MPS_MULTIPLIER = round(
        (Training.M_IN_KM / Training.MIN_IN_H ** 2), 3
    )

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при спортивной ходьбе."""
        return (
            (
                self.CALLORIES_SPORT_WALK_1 * self.weight
                + (
                    (self.get_mean_speed() * self.KPH_TO_MPS_MULTIPLIER) ** 2
                    / (self.height / self.CM_IN_M)
                )
                * self.CALLORIES_SPORT_WALK_2
                * self.weight
            )
            * self.duration
            * self.MIN_IN_H
        )


class Swimming(Training):
    """Тренировка: плавание."""
    SW_CONSTANTA_1 = 1.1
    SW_CONSTANTA_2 = 2.0
    LEN_STEP: float = 1.38

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Расчет средней скорости."""
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Количество затраченных калорий."""
        return (
            (self.get_mean_speed() + self.SW_CONSTANTA_1)
            * self.SW_CONSTANTA_2 * self.weight
            * self.duration
        )


def read_package(new_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    packages: dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if 'SWM' not in packages or 'RUN' not in packages or 'WLK' not in packages:
        raise
    return packages[new_type](*data)


def main(new_training: Training) -> None:
    """Главная функция."""
    info = new_training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: list[tuple] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
