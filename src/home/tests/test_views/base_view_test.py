from __future__ import annotations

from typing import TYPE_CHECKING, ContextManager
from unittest.mock import patch

import home.tests.test_views.utils.constants as test_view_constants
import utils.test_utils.constants as common_constants
from base.models import FollowMeLink, LegalAndPrivacy
from home.models import Education, Experience, PersonalInfo, SubProject, Technology
from utils.test_utils.base_view_test_case import BaseViewTestCase, ElementText
from utils.test_utils.constants import HtmlTag, Language
from utils.test_utils.mocks import get_date_with_mocked_today

if TYPE_CHECKING:
    from datetime import date


class BaseViewTest(BaseViewTestCase):
    @classmethod
    def _mock_on_request(cls) -> ContextManager[type[date]]:
        return patch(
            "home.models.datetime.date",
            get_date_with_mocked_today(test_view_constants.MOCKED_TODAY),
        )

    @classmethod
    def init_db(cls) -> None:
        test_technology_1 = Technology.objects.create(
            id=1,
            name=test_view_constants.TECHNOLOGY_1[Language.ENGLISH],
            name_es=test_view_constants.TECHNOLOGY_1[Language.SPANISH],
            priority=1,
        )
        test_technology_2 = Technology.objects.create(
            id=2,
            name=test_view_constants.TECHNOLOGY_2[Language.ENGLISH],
            name_es=test_view_constants.TECHNOLOGY_2[Language.SPANISH],
            priority=2,
        )
        test_technology_3 = Technology.objects.create(
            id=3,
            name=test_view_constants.TECHNOLOGY_3[Language.ENGLISH],
            name_es=test_view_constants.TECHNOLOGY_3[Language.SPANISH],
            priority=4,
        )
        test_technology_4 = Technology.objects.create(
            id=4,
            name=test_view_constants.TECHNOLOGY_4[Language.ENGLISH],
            name_es=test_view_constants.TECHNOLOGY_4[Language.SPANISH],
            priority=3,
        )

        personal_info = PersonalInfo.objects.create(
            name=test_view_constants.PERSONAL_INFO_NAME,
            title=test_view_constants.PERSONAL_INFO_TITLE[Language.ENGLISH],
            title_es=test_view_constants.PERSONAL_INFO_TITLE[Language.SPANISH],
            introduction=test_view_constants.PERSONAL_INFO_INTRODUCTION[Language.ENGLISH],
            introduction_es=test_view_constants.PERSONAL_INFO_INTRODUCTION[Language.SPANISH],
            biography=test_view_constants.PERSONAL_INFO_BIOGRAPHY[Language.ENGLISH],
            biography_es=test_view_constants.PERSONAL_INFO_BIOGRAPHY[Language.SPANISH],
        )

        personal_info.technologies.set((test_technology_1, test_technology_2, test_technology_3, test_technology_4))

        experience_1 = Experience.objects.create(
            title=test_view_constants.EXPERIENCE_1_TITLE[Language.ENGLISH],
            title_es=test_view_constants.EXPERIENCE_1_TITLE[Language.SPANISH],
            location=test_view_constants.EXPERIENCE_1_LOCATION[Language.ENGLISH],
            location_es=test_view_constants.EXPERIENCE_1_LOCATION[Language.SPANISH],
            institution=test_view_constants.EXPERIENCE_1_COMPANY,
            description=test_view_constants.EXPERIENCE_1_DESCRIPTION[Language.ENGLISH],
            description_es=test_view_constants.EXPERIENCE_1_DESCRIPTION[Language.SPANISH],
            start_date=test_view_constants.EXPERIENCE_1_START_DATE,
            end_date=test_view_constants.EXPERIENCE_1_END_DATE,
        )

        experience_1.technologies.set((test_technology_3,))

        experience_2 = Experience.objects.create(
            title=test_view_constants.EXPERIENCE_2_TITLE[Language.ENGLISH],
            title_es=test_view_constants.EXPERIENCE_2_TITLE[Language.SPANISH],
            location=test_view_constants.EXPERIENCE_2_LOCATION[Language.ENGLISH],
            location_es=test_view_constants.EXPERIENCE_2_LOCATION[Language.SPANISH],
            institution=test_view_constants.EXPERIENCE_2_COMPANY,
            description=test_view_constants.EXPERIENCE_2_DESCRIPTION[Language.ENGLISH],
            description_es=test_view_constants.EXPERIENCE_2_DESCRIPTION[Language.SPANISH],
            start_date=test_view_constants.EXPERIENCE_2_START_DATE,
        )

        experience_2.technologies.set((test_technology_4, test_technology_1, test_technology_2))

        sub_project_1 = SubProject.objects.create(
            experience=experience_2,
            title=test_view_constants.SUBPROJECT_1_TITLE[Language.ENGLISH],
            title_es=test_view_constants.SUBPROJECT_1_TITLE[Language.SPANISH],
            client=test_view_constants.SUBPROJECT_1_CLIENT,
            description=test_view_constants.SUBPROJECT_1_DESCRIPTION[Language.ENGLISH],
            description_es=test_view_constants.SUBPROJECT_1_DESCRIPTION[Language.SPANISH],
            start_date=test_view_constants.SUBPROJECT_1_START_DATE,
            end_date=test_view_constants.SUBPROJECT_1_END_DATE,
        )

        sub_project_1.technologies.set((test_technology_4, test_technology_1))

        sub_project_2 = SubProject.objects.create(
            experience=experience_2,
            title=test_view_constants.SUBPROJECT_2_TITLE[Language.ENGLISH],
            title_es=test_view_constants.SUBPROJECT_2_TITLE[Language.SPANISH],
            description=test_view_constants.SUBPROJECT_2_DESCRIPTION[Language.ENGLISH],
            description_es=test_view_constants.SUBPROJECT_2_DESCRIPTION[Language.SPANISH],
            start_date=test_view_constants.SUBPROJECT_2_START_DATE,
        )

        sub_project_2.technologies.set((test_technology_2,))

        Education.objects.create(
            id=1,
            title=test_view_constants.EDUCATION_1_TITLE[Language.ENGLISH],
            title_es=test_view_constants.EDUCATION_1_TITLE[Language.SPANISH],
            institution=test_view_constants.EDUCATION_1_INSTITUTION,
            location=test_view_constants.EDUCATION_1_LOCATION[Language.ENGLISH],
            location_es=test_view_constants.EDUCATION_1_LOCATION[Language.SPANISH],
            description=test_view_constants.EDUCATION_1_DESCRIPTION[Language.ENGLISH],
            description_es=test_view_constants.EDUCATION_1_DESCRIPTION[Language.SPANISH],
            start_date=test_view_constants.EDUCATION_1_START_DATE,
            end_date=test_view_constants.EDUCATION_1_END_DATE,
        )

        Education.objects.create(
            id=2,
            title=test_view_constants.EDUCATION_2_TITLE[Language.ENGLISH],
            title_es=test_view_constants.EDUCATION_2_TITLE[Language.SPANISH],
            institution=test_view_constants.EDUCATION_2_INSTITUTION,
            location=test_view_constants.EDUCATION_2_LOCATION[Language.ENGLISH],
            location_es=test_view_constants.EDUCATION_2_LOCATION[Language.SPANISH],
            description=test_view_constants.EDUCATION_2_DESCRIPTION[Language.ENGLISH],
            description_es=test_view_constants.EDUCATION_2_DESCRIPTION[Language.SPANISH],
            start_date=test_view_constants.EDUCATION_2_START_DATE,
            end_date=test_view_constants.EDUCATION_2_END_DATE,
        )

        LegalAndPrivacy.objects.create(
            title=test_view_constants.LEGAL_SECTION_1[Language.ENGLISH],
            title_es=test_view_constants.LEGAL_SECTION_1[Language.SPANISH],
            text=test_view_constants.LEGAL_TEXT_1[Language.ENGLISH],
            text_es=test_view_constants.LEGAL_TEXT_1[Language.SPANISH],
        )

        LegalAndPrivacy.objects.create(
            title=test_view_constants.LEGAL_SECTION_2[Language.ENGLISH],
            title_es=test_view_constants.LEGAL_SECTION_2[Language.SPANISH],
            text=test_view_constants.LEGAL_TEXT_2[Language.ENGLISH],
            text_es=test_view_constants.LEGAL_TEXT_2[Language.SPANISH],
        )

        FollowMeLink.objects.create(
            name=test_view_constants.FOLLOW_ME_LINK_NAME,
            link=test_view_constants.FOLLOW_ME_LINK,
            svg_view_box=test_view_constants.FOLLOW_ME_LINK_VIEW_BOX,
            svg_path=test_view_constants.FOLLOW_ME_LINK_PATH,
        )

    def test_legal_and_privacy(self) -> None:
        legal_and_privacy_section = self._find_element_by_tag_and_id(
            self._find_element_by_tag_and_id(
                self.response_data.soup, HtmlTag.FOOTER, test_view_constants.UPPER_FOOTER_ID
            ),
            HtmlTag.NAV,
            test_view_constants.LEGAL_AND_PRIVACY_ID,
        )

        self._assert_text_of_element_by_tag_and_id(
            legal_and_privacy_section,
            html_tag=HtmlTag.H6,
            element_id=test_view_constants.LEGAL_AND_PRIVACY_TITLE_ID,
            expected_text=test_view_constants.LEGAL_AND_PRIVACY_TITLE[self.language],
        )

        self._assert_text_of_elements(
            legal_and_privacy_section,
            ElementText(
                html_tag=HtmlTag.BUTTON,
                element_id=test_view_constants.LEGAL_AND_PRIVACY_LINK_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.LEGAL_SECTION_1[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.BUTTON,
                element_id=test_view_constants.LEGAL_AND_PRIVACY_LINK_ID_TEMPLATE.format(id=2),
                expected_text=test_view_constants.LEGAL_SECTION_2[self.language],
            ),
        )

        self._assert_attribute_of_element(
            self._find_element_by_tag_and_id(
                legal_and_privacy_section,
                HtmlTag.BUTTON,
                test_view_constants.LEGAL_AND_PRIVACY_LINK_ID_TEMPLATE.format(id=1),
            ),
            common_constants.ATTR_ONCLICK,
            f"{test_view_constants.LEGAL_AND_PRIVACY_MODAL_ID_TEMPLATE.format(id=1)}.showModal()",
        )

        self._assert_attribute_of_element(
            self._find_element_by_tag_and_id(
                legal_and_privacy_section,
                HtmlTag.BUTTON,
                test_view_constants.LEGAL_AND_PRIVACY_LINK_ID_TEMPLATE.format(id=2),
            ),
            common_constants.ATTR_ONCLICK,
            f"{test_view_constants.LEGAL_AND_PRIVACY_MODAL_ID_TEMPLATE.format(id=2)}.showModal()",
        )

        self._assert_text_of_elements(
            self._find_element_by_tag_and_id(
                legal_and_privacy_section,
                html_tag=HtmlTag.DIALOG,
                element_id=test_view_constants.LEGAL_AND_PRIVACY_MODAL_ID_TEMPLATE.format(id=1),
            ),
            ElementText(
                html_tag=HtmlTag.H1,
                element_id=test_view_constants.LEGAL_AND_PRIVACY_TITLE_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.LEGAL_SECTION_1[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.LEGAL_AND_PRIVACY_TEXT_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.LEGAL_TEXT_1[self.language],
            ),
        )

        self._assert_text_of_elements(
            self._find_element_by_tag_and_id(
                legal_and_privacy_section,
                html_tag=HtmlTag.DIALOG,
                element_id=test_view_constants.LEGAL_AND_PRIVACY_MODAL_ID_TEMPLATE.format(id=2),
            ),
            ElementText(
                html_tag=HtmlTag.H1,
                element_id=test_view_constants.LEGAL_AND_PRIVACY_TITLE_ID_TEMPLATE.format(id=2),
                expected_text=test_view_constants.LEGAL_SECTION_2[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.LEGAL_AND_PRIVACY_TEXT_ID_TEMPLATE.format(id=2),
                expected_text=test_view_constants.LEGAL_TEXT_2[self.language],
            ),
        )

    def test_follow_me_links(self) -> None:
        follow_me_links_section = self._find_element_by_tag_and_id(
            self._find_element_by_tag_and_id(
                self.response_data.soup, HtmlTag.FOOTER, test_view_constants.UPPER_FOOTER_ID
            ),
            HtmlTag.NAV,
            test_view_constants.FOLLOW_ME_LINKS_ID,
        )

        self._assert_text_of_element_by_tag_and_id(
            follow_me_links_section,
            html_tag=HtmlTag.H6,
            element_id=test_view_constants.FOLLOW_ME_LINKS_TITLE_ID,
            expected_text=test_view_constants.FOLLOW_ME_LINKS_TITLE[self.language],
        )

        follow_me_link_container = self._find_element_by_tag_and_id(
            follow_me_links_section,
            html_tag=HtmlTag.DIV,
            element_id=test_view_constants.FOLLOW_ME_LINK_CONTAINER_ID_TEMPLATE.format(id=1),
        )
        self._assert_element_contains_class_name(follow_me_link_container, common_constants.CLASS_TOOLTIP)
        self._assert_attribute_of_element(
            follow_me_link_container,
            common_constants.ATTR_DATA_TIP,
            test_view_constants.FOLLOW_ME_LINK_NAME,
        )

        follow_me_link = self._find_element_by_tag_and_id(
            follow_me_link_container,
            html_tag=HtmlTag.A,
            element_id=test_view_constants.FOLLOW_ME_LINK_ID_TEMPLATE.format(id=1),
        )
        self._assert_attribute_of_element(
            follow_me_link,
            common_constants.ATTR_HREF,
            test_view_constants.FOLLOW_ME_LINK,
        )
        self._assert_attribute_of_element(follow_me_link, common_constants.ATTR_TARGET, "_blank")

        follow_me_link_svg = self._find_element_by_html_tag(follow_me_link, html_tag=HtmlTag.SVG)
        self._assert_attribute_of_element(
            follow_me_link_svg,
            common_constants.ATTR_VIEW_BOX,
            test_view_constants.FOLLOW_ME_LINK_VIEW_BOX,
        )

        follow_me_link_path = self._find_element_by_html_tag(follow_me_link_svg, html_tag=HtmlTag.PATH)
        self._assert_attribute_of_element(
            follow_me_link_path,
            common_constants.ATTR_D,
            test_view_constants.FOLLOW_ME_LINK_PATH,
        )

    def test_source_code_note(self) -> None:
        bottom_footer = self._find_element_by_tag_and_id(
            self.response_data.soup, HtmlTag.FOOTER, test_view_constants.BOTTOM_FOOTER_ID
        )

        self._assert_text_of_element_by_tag_and_id(
            bottom_footer,
            html_tag=HtmlTag.ASIDE,
            element_id=test_view_constants.SOURCE_CODE_NOTE_ID,
            expected_text=test_view_constants.SOURCE_CODE_NOTE_TEXT[self.language],
        )

        self._assert_attribute_of_element(
            self._find_element_by_tag_and_id(
                bottom_footer,
                HtmlTag.A,
                test_view_constants.GITHUB_REPO_LINK_ID,
            ),
            common_constants.ATTR_HREF,
            test_view_constants.SOURCE_CODE_GITHUB_LINK,
        )

    def test_seo_canonical_url(self) -> None:
        """Test that canonical URL points to the correct page."""
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.LINK, "rel", "canonical"),
            "href",
            f"http://testserver/{self.language}/{self.request_path}",
        )

    def test_seo_hreflang_tags(self) -> None:
        """Test that hreflang tags are correct for home page."""
        hreflang_tags = self.response_data.soup.find_all("link", attrs={"rel": "alternate"})

        hreflang_en = next((tag for tag in hreflang_tags if tag.get("hreflang") == "en"), None)
        hreflang_es = next((tag for tag in hreflang_tags if tag.get("hreflang") == "es"), None)
        hreflang_default = next((tag for tag in hreflang_tags if tag.get("hreflang") == "x-default"), None)

        assert hreflang_en is not None, "Hreflang tag for 'en' should exist"
        assert hreflang_es is not None, "Hreflang tag for 'es' should exist"
        assert hreflang_default is not None, "Hreflang tag for 'x-default' should exist"

        self._assert_attribute_of_element(hreflang_en, "href", f"http://testserver/en/{self.request_path}")
        self._assert_attribute_of_element(hreflang_es, "href", f"http://testserver/es/{self.request_path}")
        self._assert_attribute_of_element(hreflang_default, "href", f"http://testserver/en/{self.request_path}")
