try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from .form_input import FormInput
from .textarea import TextArea


class Form(object):
    def __init__(self, url, document):
        self.document = document
        self.action = urljoin(url, document.attrib.get('action'))
        self.parameters = {}

    def get_inputs(self):
        for input_element in self.get_input_elements():
            yield FormInput(input_element)

        for textarea in self.get_textarea_elements():
            yield TextArea(input_element)

    def get_parameters(self):
        for item in self.get_inputs():
            yield item.get_name(), item.guess_value()

    def get_input_elements(self):
        for form_input in self.document.findall('.//input[@type]'):
            yield form_input

    def get_textarea_elements(self):
        for textarea in self.document.findall('.//textarea'):
            yield textarea

    def send(self, client, parameters):
        return client.download_page(self.action, parameters)