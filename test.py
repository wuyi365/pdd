#request_url = 'http://apiv2.yangkeduo.com/api/oak/v6/goods/'+ str(goods_id)+ '?goods_id=' + str(goods_id) + '&pdduid='

def get_url(goods_id):
    return 'http://apiv2.yangkeduo.com/api/oak/v6/goods/'+ str(goods_id)+ '?goods_id=' + str(goods_id) + '&pdduid='

a = [628563806, 53564917]

c = list(map(get_url, a))
print(c)