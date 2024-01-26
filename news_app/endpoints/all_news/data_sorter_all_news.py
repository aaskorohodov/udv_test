import datetime

from news_app.endpoints.support.abstract_sorters import ABSSorter
from news_app.models.internal.news import NewsItem
from news_app.models.response.all_news_response.news_listed import NewsResponse


class DataSorter(ABSSorter):
    """Готовит данные со всеми новостями, превращает все в единственную модель, готовую к отправке"""

    def make_news_list(self) -> NewsResponse:
        """Строит новость из имеющихся сырых данных и возвращает ее в виде модели, готовой к отправке"""

        self._convert_data()
        self._map_comments()
        response_model = self._fill_response_model()

        return response_model

    def _fill_response_model(self) -> NewsResponse:
        """Создает модель для отправки клиенту и наполняет ее данными

        Returns:
            NewsResponse, полностью готовую к отправке"""

        # Модель для возврата клиенту
        response_news_model = NewsResponse()

        # Перебираем имеющиеся новости, проверяем что они пригодны к отправке, кладем в модель
        current_dt = datetime.datetime.now()
        for single_news in self.news_dict.values():
            if self._check_conditions(single_news, current_dt):
                response_news = single_news.to_response_model_all_news()
                response_news_model.news.append(response_news)

        # Сортируем новости по дате и считаем их
        response_news_model.sort_news_by_date()
        response_news_model.count_news()

        return response_news_model

    def _check_conditions(self, single_news: NewsItem, current_dt: datetime.datetime) -> bool:
        """Проверяет, что новость можно отправить клиенту

        Args:
            single_news: Проверяемая новость
            current_dt: Дата, считающаяся текущей
        Returns:
            True, если отправить такую новость можно"""

        if single_news.deleted:
            return False
        if single_news.date > current_dt:
            return False

        return True
