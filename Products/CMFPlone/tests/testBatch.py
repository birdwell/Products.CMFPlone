from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from Products.CMFPlone.PloneBatch import Batch
from Products.CMFPlone.tests.CMFPloneTestCase import CMFPloneTestCase
from Products.CMFPlone.tests.layers import PLONE_TEST_CASE_INTEGRATION_TESTING
from Products.ZCatalog.Lazy import LazyMap

class TestBatch(CMFPloneTestCase):

    layer = PLONE_TEST_CASE_INTEGRATION_TESTING

    def test_batch_no_lazy(self):
        batch = Batch(range(100), size=10, start=10)
        self.assertEqual([b for b in batch],
            [10, 11, 12, 13, 14, 15, 16, 17, 18, 19])

    def test_batch_lazy_map(self):
        def get(key):
            return key
        sequence = LazyMap(get, range(80, 90), actual_result_count=95)
        batch = Batch(sequence, size=10, start=80)
        self.assertEqual([b for b in batch],
            [80, 81, 82, 83, 84, 85, 86, 87, 88, 89])

        self.assertEqual(batch.numpages, 10)
        self.assertEqual(batch.pagenumber, 9)
        self.assertEqual(batch.navlist, [6, 7, 8, 9, 10])
        self.assertEqual(batch.leapback, [])
        self.assertEqual(batch.prevlist, [6, 7, 8])
        self.assertEqual(batch.previous.length, 10)
        self.assertEqual(batch.next.length, 5)
        self.assertEqual(batch.pageurl({}), 'b_start:int=80')
        self.assertEqual(batch.prevurls({}),
            [(6, 'b_start:int=50'), (7, 'b_start:int=60'),
            (8, 'b_start:int=70')])
        self.assertEqual(batch.nexturls({}), [(10, 'b_start:int=90')])

    def test_batch_brains(self):
        portal = self.layer['portal']
        login(portal, TEST_USER_NAME)
        setRoles(portal, TEST_USER_ID, ['Manager'])

        for obj_id in ['AAA%stest' % chr(c) for c in range(97, 123)]:
            portal.invokeFactory('Document', obj_id)

        brains = portal.portal_catalog.searchResults(portal_type='Document',
                                                     sort_on='id')
        batch = Batch(brains, size=10, start=10)
        self.assertEqual(batch[0].id, 'AAAktest')
