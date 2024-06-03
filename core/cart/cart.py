from stylist.models import Services,ServiceStatusType
from cart.models import CartModel,CartItemModel

class CartSession:
    def __init__(self, session):
        self.session = session
        self._cart = self.session.setdefault("cart", {"items": []})

    def update_service_quantity(self,service_id,quantity):
        for item in self._cart["items"]:
            if service_id == item["service_id"]:
                item["quantity"] = int(quantity)
                break
        else:
            return
        self.save()
    
    def remove_service(self,service_id):
        for item in self._cart["items"]:
            if service_id == item["service_id"]:
                self._cart["items"].remove(item)
                break
        else:
            return
        self.save()
        
    def add_service(self, service_id):
        for item in self._cart["items"]:
            if service_id == item["service_id"]:
                item["quantity"] += 1
                break
        else:
            new_item = {"service_id": service_id, "quantity": 1}
            self._cart["items"].append(new_item)
        self.save()

    def clear(self):
        self._cart = self.session["cart"] = {"items": []}
        self.save()

    def get_cart_dict(self):
        return self._cart

    def get_cart_items(self):
        for item in self._cart["items"]:
            service_obj = Services.objects.get(id=item["service_id"], status=ServiceStatusType.publish.value)
            item.update({"service_obj": service_obj, "total_price": item["quantity"] * service_obj.get_price()})

        return self._cart["items"]

    def get_total_payment_amount(self):
        return sum(item["total_price"] for item in self._cart["items"])

    def get_total_quantity(self):
        return sum(item["quantity"] for item in self._cart["items"])

    def save(self):
        self.session.modified = True


    def sync_cart_items_from_db(self,user):
        cart,created = CartModel.objects.get_or_create(user=user)
        cart_items = CartItemModel.objects.filter(cart=cart)
        
        for cart_item in cart_items:
            for item in self._cart["items"]:
                if str(cart_item.service.id) == item["service_id"]:
                    cart_item.quantity = item["quantity"]
                    cart_item.save()
                    break
            else:
                new_item = {"service_id": str(cart_item.service.id), "quantity": cart_item.quantity}
                self._cart["items"].append(new_item)
        self.merge_session_cart_in_db(user)
        self.save()
            
        
    def merge_session_cart_in_db(self,user):
        cart,created = CartModel.objects.get_or_create(user=user)
        
        for item in  self._cart["items"]:
            service_obj = Services.objects.get(id=item["service_id"], status=ServiceStatusType.publish.value)
            
            cart_item ,created = CartItemModel.objects.get_or_create(cart=cart,service=service_obj)
            cart_item.quantity = item["quantity"]
            cart_item.save()
        session_service_ids = [item["service_id"] for item in  self._cart["items"]]
        CartItemModel.objects.filter(cart=cart).exclude(service__id__in=session_service_ids).delete()
        

        