class DBRouter:
    def db_for_read(self, model, **hints):
        print(f"Reading from: {model._meta.app_label}")
        if model._meta.app_label == 'trademarks':
            return 'trademarks_db'
        return 'default'

    def db_for_write(self, model, **hints):
        print(f"Writing to: {model._meta.app_label}")
        if model._meta.app_label == 'trademarks':
            return 'trademarks_db'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        print(f"Allow relation between: {obj1._meta.app_label} and {obj2._meta.app_label}")
        if obj1._meta.app_label == 'trademarks' or obj2._meta.app_label == 'trademarks':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        print(f"Allow migrate: db={db}, app_label={app_label}")
        if app_label == 'trademarks':
            return db == 'trademarks_db'
        return db == 'default'
