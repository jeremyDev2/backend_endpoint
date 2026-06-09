from locust import HttpUser, task

class PurchaseUser(HttpUser):
    @task
    def purchase(self):
        self.client.post("/purchase", json={ "user_id": 1,
                                            "product_id": 1,
                                            "purchased_count": 1})
