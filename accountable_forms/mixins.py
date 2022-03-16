from accountable_forms.models import AFPrefix, AFTransactionStatus, AFItem


class BaseRepresentAFMixin:

    def to_represent_af(self, instance):
        instance['prefix'] = AFPrefix.objects.get(pk=instance['prefix']).name
        instance['status'] = AFTransactionStatus.objects.get(pk=instance['status']).name

        return instance


class PurchaseTransactionMixin:
    purchase_item_class = None

    def get_purchase_entry(self, data):
        raise NotImplementedError

    def get_transaction_type(self, history):
        raise NotImplementedError

    def to_represent_purchase_item(self, entry, item):
        raise NotImplementedError

    def create_purchase_item(self, data):
        purchase_item = self.purchase_item_class.objects.create(**data)
        return purchase_item

    def add_purchase_item(self, history, item, entry):
        purchase_item_data = self.to_represent_purchase_item(entry, item)
        purchase_item = self.create_purchase_item(purchase_item_data)

        return purchase_item

    def create_history_item(self, history, data):
        transaction_type = self.get_transaction_type(history)

        if transaction_type != 'TYPE_PURCHASE':
            return super().create_history_item(history, data)

        entry = self.get_purchase_entry(data)
        transaction_item = super().create_history_item(history, data)

        # add AF Purchase Item to DB
        purchase_item = self.add_purchase_item(history, transaction_item, entry)

        # add AF Items to inventory
        self.add_af_item(history, purchase_item, transaction_item)

        return transaction_item

    def add_af_item(self, history, purchase_item, transaction_item):
        raise NotImplementedError


class AFItemPurchaseMixin:
    DEFAULT_STUB_LENGTH = 50

    def add_af_item(self, history, purchase_item, transaction_item):

        total_quantity = transaction_item.quantity * self.DEFAULT_STUB_LENGTH
        for index in range(total_quantity):
            self.create_af_item(history, purchase_item, transaction_item, index)

    def calculate_end_series(self, start_series, quantity):
        return quantity * self.DEFAULT_STUB_LENGTH + start_series - 1

    def create_af_item(self, history, purchase_item, transaction_item, index):
        af_item = AFItem.objects.create(
            af_type=transaction_item.af_type,
            ownership=history.issued_to,
            start_series=purchase_item.start_series,
            current_series=purchase_item.start_series+index,
            end_series=self.calculate_end_series(purchase_item.start_series, transaction_item.quantity),
            stub_number=purchase_item.stub_number,
            prefix=purchase_item.prefix,
            suffix=purchase_item.suffix
        )
        return af_item


