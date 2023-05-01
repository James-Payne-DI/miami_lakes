import falcon, json

# class CompaniesResource(object):
#     companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]
#     def on_get(self, req, resp):
#         resp.body = json.dumps(self.companies)
#     def on_post(self, req, resp):
#         resp.status = falcon.HTTP_201
#         resp.body = json.dumps({"success": True})
#
#
# api = falcon.API()
# companies_endpoint = CompaniesResource()
# api.add_route('/companies', companies_endpoint)


class yoastResource(object):
    def __init__(self,metaTitle,metaDesc):
        self.metaData = [{"title": metaTitle, "description": metaDesc,"og_title": metaTitle,"og_description": metaDesc}]
    def on_get(self, req, resp):
        resp.body = json.dumps(self.metaData)
    def on_post(self, req, resp):
        resp.status = falcon.HTTP_201
        resp.body = json.dumps({"success": True})

# api = falcon.App()
# meta_endpoint = yoastResource(metaTitle="Test Title",metaDesc="lorem Test description yo yo yo")
# api.add_route('/custom_meta', meta_endpoint)
