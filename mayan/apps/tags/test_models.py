from __future__ import unicode_literals

import os

from django.conf import settings
from django.core.files.base import File
from django.test import TestCase

from documents.models import Document, DocumentType
from documents.test_models import TEST_DOCUMENT_TYPE

from .literals import COLOR_RED
from .models import Tag

TEST_DOCUMENT_PATH = os.path.join(settings.BASE_DIR, 'contrib', 'sample_documents', 'title_page.png')


class TagTestCase(TestCase):
    def setUp(self):
        self.document_type = DocumentType.objects.create(label=TEST_DOCUMENT_TYPE)

        ocr_settings = self.document_type.ocr_settings
        ocr_settings.auto_ocr = False
        ocr_settings.save()

        with open(TEST_DOCUMENT_PATH) as file_object:
            self.document = self.document_type.new_document(file_object=File(file_object))

    def tearDown(self):
        self.document.delete()
        self.document_type.delete()

    def runTest(self):
        tag = Tag(label='test', color=COLOR_RED)
        tag.save()
        self.assertEqual(tag.label, 'test')
        self.assertEqual(tag.get_color_code(), 'red')

    def test_addition_and_deletion_of_documents(self):
        tag = Tag(label='test', color=COLOR_RED)
        tag.save()

        tag.documents.add(self.document)

        self.assertEqual(tag.documents.count(), 1)
        self.assertEqual(list(tag.documents.all()), [self.document])

        tag.documents.remove(self.document)

        self.assertEqual(tag.documents.count(), 0)
        self.assertEqual(list(tag.documents.all()), [])

        tag.delete()
