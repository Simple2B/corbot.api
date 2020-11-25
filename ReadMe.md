# CorBot API

## How to add modules

1. Add module file of module folder to `app/controllers` folder. E.g. `app/controllers/runner` - python module folder.
1. Import Register class:

    ```python
    from app.controllers.register import Register
    ```

1. Create Register instance with class name:

    ```python
    runner = Register("Runner")
    ```

1. Declare python function as request handler:

    ```python
    @runner.register()
    def service_ident(data):
        pass
    ```

    1. Decorator `@runner.register()` uses for registration this python function as API request handler
    1. Function must by follow prototype:

        ```python
        def request_name(data: dict) -> dict:
            return {}
        ```

    1. If need use different request name, use `name` argument in decorator. For example:

        ```python
        @runner.register(name="request_name")
        def func_name(data):
            pass
        ```
