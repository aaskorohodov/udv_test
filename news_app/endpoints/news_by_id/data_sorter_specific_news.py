import datetime

from fastapi import HTTPException, status

from news_app.endpoints.support.abstract_sorters import ABSSorter
from news_app.models.response.news_by_id_response.specific_news import SpecificNews


class SpecificNewsDataSorter(ABSSorter):
    """Сортировщик, который готовит данные для получения конкретной новости"""

    def get_specific_news(self, news_id: int) -> SpecificNews:
        """Отдает модель, готовую к отправке, для конкретной новости

        Args:
            news_id: id новости, которую хочет клиент
        Returns:
            Модель конкретной новости, готовую к отправке"""

        self._convert_data()
        self._check_news_is_ok(news_id)
        self._map_comments()

        requested_news = self.news_dict[news_id]

        return requested_news.to_response_model_news_by_id()

    def _check_news_is_ok(self, news_id: int) -> None:
        """Проверяет, что запрошенную новость можно отправить

        Args:
            news_id: id запрошенной новости
        Raises:
            HTTPException: с сообщением, согласно случившейся ситуации"""

        # Такой новости нет
        error_msg = ''
        if news_id not in self.news_dict:
            error_msg += f'No such news with id {news_id} found in our shiny DB!\n'

        requested_news = self.news_dict.get(news_id)
        if requested_news:
            # Новость удалена
            if requested_news.deleted:
                error_msg += f'News with id {news_id} was deleted! We are very sorry.\n'

            # Дата новости еще не наступила
            current_dt = datetime.datetime.now()
            if requested_news.date > current_dt:
                error_msg += f'News with id {news_id} is not ready for publication yet, but it will be on ' \
                             f'{requested_news.date.__str__()}, wait a bit please!\n'

        if error_msg:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)
