from sqladmin import ModelView

from models import News, Service, FAQ, ClientRequest


class NewsAdmin(ModelView, model=News):
    name = "Новость"
    name_plural = "Новости"
    icon = "fa-solid fa-newspaper"
    column_list = [News.id, News.title, News.created_at]
    column_searchable_list = [News.title]
    column_sortable_list = [News.id, News.created_at]
    column_default_sort = [(News.created_at, True)]
    form_columns = [News.title, News.content]


class ServiceAdmin(ModelView, model=Service):
    name = "Услуга"
    name_plural = "Услуги"
    icon = "fa-solid fa-briefcase"
    column_list = [Service.id, Service.title, Service.price, Service.order]
    column_sortable_list = [Service.id, Service.order]
    form_columns = [Service.title, Service.description, Service.price, Service.order]


class FAQAdmin(ModelView, model=FAQ):
    name = "Вопрос FAQ"
    name_plural = "FAQ"
    icon = "fa-solid fa-circle-question"
    column_list = [FAQ.id, FAQ.question, FAQ.order]
    column_sortable_list = [FAQ.id, FAQ.order]
    form_columns = [FAQ.question, FAQ.answer, FAQ.order]


class ClientRequestAdmin(ModelView, model=ClientRequest):
    name = "Заявка"
    name_plural = "Заявки клиентов"
    icon = "fa-solid fa-envelope"
    column_list = [
        ClientRequest.id,
        ClientRequest.name,
        ClientRequest.phone,
        ClientRequest.status,
        ClientRequest.created_at,
    ]
    column_sortable_list = [ClientRequest.id, ClientRequest.created_at]
    column_default_sort = [(ClientRequest.created_at, True)]
    column_searchable_list = [ClientRequest.name, ClientRequest.phone]
    form_columns = [
        ClientRequest.name,
        ClientRequest.phone,
        ClientRequest.message,
        ClientRequest.status,
    ]
    # Make it read-friendly: new requests are highlighted
    column_labels = {
        ClientRequest.status: "Статус",
        ClientRequest.name: "Имя",
        ClientRequest.phone: "Телефон",
        ClientRequest.message: "Сообщение",
        ClientRequest.created_at: "Дата",
    }
