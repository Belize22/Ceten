class ResourceBank:
    def __init__(self, starting_quantity=0):
        self.resources = []
        self.resource_buffers = []

        for i in range(5):
            self.resources.append(starting_quantity)
            self.resource_buffers.append(0)

    # TODO: Pass the resource as enum instead of string.
    def deposit_resource(self, resource, quantity):
        self.resource_buffers[resource] += quantity

    def withdraw_resource(self, resource, quantity):
        self.resource_buffers[resource] -= quantity

    def collect_resources(self, resources_spent):
        for i in range(len(self.resources)):
            self.resource_buffers[i] += resources_spent[i]

    def spend_resources(self, resources_spent):
        for i in range(len(self.resources)):
            self.resource_buffers[i] -= resources_spent[i]
    
    def validate_transaction(self):
        transaction_valid = True
        for i in range(len(self.resources)):
            if self.resources[i] + self.resource_buffers[i] < 0:
                transaction_valid = False
                break
        if transaction_valid:
            self.confirm_transaction()
        self.clear_buffers()
        return transaction_valid
   
    def confirm_transaction(self):
        for i in range(len(self.resources)):
            self.resources[i] += self.resource_buffers[i]

    def cancel_transaction(self):
        self.clear_buffers()
        
    def clear_buffers(self):
        for i in range(len(self.resources)):
            self.resource_buffers[i] = 0

