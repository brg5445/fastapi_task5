class BaseDomainException(Exception):
    def __init__(self, detail: str) -> None:
        self._detail = detail

    def get_detail(self) -> str:
        return self._detail


class UserNotFoundByNicknameException(BaseDomainException):
    _exception_text_template = "Пользователь с никнеймом='{nickname}' не найден."

    def __init__(self, nickname: str) -> None:
        self._exception_text_template = self._exception_text_template.format(nickname=nickname)

        super().__init__(detail=self._exception_text_template)


class UserNicknameIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Пользователь с никнеймом='{nickname}' уже существует."

    def __init__(self, nickname: str) -> None:
        self._exception_text_template = self._exception_text_template.format(nickname=nickname)

        super().__init__(detail=self._exception_text_template)


class UserEmailIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Пользователь с почтой='{email}' уже существует."

    def __init__(self, email: str) -> None:
        self._exception_text_template = self._exception_text_template.format(email=email)

        super().__init__(detail=self._exception_text_template)


class CategoryNotFoundBySlugException(BaseDomainException):
    _exception_text_template = "Категория с названием='{slug}' не найдена."

    def __init__(self, slug: str) -> None:
        self._exception_text_template = self._exception_text_template.format(slug=slug)

        super().__init__(detail=self._exception_text_template)


class CategoryIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Категория с названием='{slug}' уже существует."

    def __init__(self, slug: str) -> None:
        self._exception_text_template = self._exception_text_template.format(slug=slug)

        super().__init__(detail=self._exception_text_template)


class LocationNotFoundByNameException(BaseDomainException):
    _exception_text_template = "Локация с названием='{name}' не найдена."

    def __init__(self, name: str) -> None:
        self._exception_text_template = self._exception_text_template.format(name=name)

        super().__init__(detail=self._exception_text_template)


class LocationIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Категория с названием='{name}' уже существует."

    def __init__(self, name: str) -> None:
        self._exception_text_template = self._exception_text_template.format(name=name)

        super().__init__(detail=self._exception_text_template)


class PostNotFoundByIDException(BaseDomainException):
    _exception_text_template = "Пост с id='{id}' не найден."

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(id=id)

        super().__init__(detail=self._exception_text_template)


class PostDontCreateException(BaseDomainException):
    _exception_text_template = "Пост не смог быть создан, так как {cause}."

    def __init__(self, cause: str) -> None:
        self._exception_text_template = self._exception_text_template.format(cause=cause)

        super().__init__(detail=self._exception_text_template)


class PostDontChangeException(BaseDomainException):
    _exception_text_template = "Пост не смог быть изменён, так как {cause}."

    def __init__(self, cause: str) -> None:
        self._exception_text_template = self._exception_text_template.format(cause=cause)

        super().__init__(detail=self._exception_text_template)


class CommentNotFoundByIDException(BaseDomainException):
    _exception_text_template = "Комментарий с id='{id}' не найден."

    def __init__(self, id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(id=id)

        super().__init__(detail=self._exception_text_template)


class CommentDontCreateException(BaseDomainException):
    _exception_text_template = "Комментарий не смог быть создан, так как {cause}."

    def __init__(self, cause: str) -> None:
        self._exception_text_template = self._exception_text_template.format(cause=cause)

        super().__init__(detail=self._exception_text_template)


# class CommentDontChangeException(BaseDomainException):
#     _exception_text_template = "Комментарий не смог быть изменён, так как {cause}."

#     def __init__(self, cause: str) -> None:
#         self._exception_text_template = self._exception_text_template.format(cause=cause)

#         super().__init__(detail=self._exception_text_template)