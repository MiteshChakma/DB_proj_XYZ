class FinlandSwedenRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'finland_app':
            return 'finland'
        elif model._meta.app_label == 'sweden_app':
            return 'sweden'
        return 'default'

    def db_for_write(self, model, **hints):
        return self.db_for_read(model, **hints)

    # ... other router methods ...
