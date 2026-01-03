from __future__ import annotations

from django.test import TestCase

import home.tests.test_views.utils.constants as test_view_constants
import utils.test_utils.constants as common_constants
from home.tests.test_views.base_view_test import BaseViewTest
from utils.test_utils.base_view_test_case import ElementText
from utils.test_utils.constants import HtmlTag, Language


class TestHomeViewBasics(TestCase):
    def test_home_view_redirects(self) -> None:
        response = self.client.get("/my-career/")
        self.assertRedirects(response, "/en/my-career/", status_code=302, target_status_code=200)


class BaseTestMyCareerViewContent(BaseViewTest):
    request_path = "my-career/"

    def test_response(self) -> None:
        self._assert_reponse_status_code(expected_status_code=200)
        self._assert_template_is_used("my-career.html")
        self._assert_template_is_used("cotton/experience_timeline.html")
        self._assert_template_is_used("cotton/base.html")

    def test_experiences(self) -> None:
        my_career = self._find_element_by_id(self.response_data.soup, test_view_constants.MY_CAREER_ID)

        self._assert_text_of_element(
            my_career,
            HtmlTag.H1,
            test_view_constants.MY_CAREER_TITLE_ID,
            test_view_constants.MY_CAREER_TITLE[self.language],
        )

        experiences = self._find_element_by_id(my_career, element_id=test_view_constants.EXPERIENCES_LIST_ID).find_all(
            HtmlTag.LI
        )

        self.assertEqual(
            number_of_experiences := len(experiences),
            test_view_constants.EXPECTED_NUMBER_OF_EXPERIENCES,
            f"There should be {test_view_constants.EXPECTED_NUMBER_OF_EXPERIENCES}"
            f" experiences, but there are {number_of_experiences}",
        )

        self._assert_text_of_elements(
            experiences[0],
            ElementText(
                html_tag=HtmlTag.TIME,
                element_id=test_view_constants.EXPERIENCE_PERIOD_ID_TEMPLATE.format(id=2),
                expected_text=test_view_constants.EXPERIENCE_2_PERIOD[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.EXPERIENCE_DURATION_ID_TEMPLATE.format(id=2),
                expected_text=test_view_constants.EXPERIENCE_2_DURATION[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.EXPERIENCE_TITLE_ID_TEMPLATE.format(id=2),
                expected_text=test_view_constants.EXPERIENCE_2_TITLE[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.EXPERIENCE_INSTITUTION_ID_TEMPLATE.format(id=2),
                expected_text=test_view_constants.EXPERIENCE_2_COMPANY,
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.EXPERIENCE_LOCATION_ID_TEMPLATE.format(id=2),
                expected_text=test_view_constants.EXPERIENCE_2_LOCATION[self.language],
            ),
        )

        self._assert_list_of_strings(
            self._find_element_by_id(
                experiences[0], test_view_constants.EXPERIENCE_TECHNOLOGIES_ID_TEMPLATE.format(id=2)
            ),
            [
                test_view_constants.TECHNOLOGY_1[self.language],
                test_view_constants.TECHNOLOGY_2[self.language],
                test_view_constants.TECHNOLOGY_4[self.language],
            ],
        )

        self._assert_attribute_of_element(
            self._find_element_by_tag_and_id(
                experiences[0],
                HtmlTag.BUTTON,
                test_view_constants.EXPERIENCE_MORE_BUTTON_ID_TEMPLATE.format(id=2),
            ),
            common_constants.ATTR_ONCLICK,
            f"{test_view_constants.EXPERIENCE_MODAL_ID_TEMPLATE.format(id=2)}.showModal()",
        )

        self._assert_text_of_elements(
            self._find_element_by_tag_and_id(
                experiences[0],
                HtmlTag.DIALOG,
                test_view_constants.EXPERIENCE_MODAL_ID_TEMPLATE.format(id=2),
            ),
            ElementText(
                html_tag=HtmlTag.TIME,
                element_id=test_view_constants.MODAL_EXPERIENCE_PERIOD_ID_TEMPLATE.format(id=2),
                expected_text=test_view_constants.EXPERIENCE_2_PERIOD[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.MODAL_EXPERIENCE_DURATION_ID_TEMPLATE.format(id=2),
                expected_text=test_view_constants.EXPERIENCE_2_DURATION[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.H3,
                element_id=test_view_constants.MODAL_EXPERIENCE_TITLE_ID_TEMPLATE.format(id=2),
                expected_text=test_view_constants.EXPERIENCE_2_TITLE[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.MODAL_EXPERIENCE_INSTITUTION_ID_TEMPLATE.format(id=2),
                expected_text=test_view_constants.EXPERIENCE_2_COMPANY,
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.MODAL_EXPERIENCE_LOCATION_ID_TEMPLATE.format(id=2),
                expected_text=test_view_constants.EXPERIENCE_2_LOCATION[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.MODAL_EXPERIENCE_DESCRIPTION_ID_TEMPLATE.format(id=2),
                expected_text=test_view_constants.EXPERIENCE_2_DESCRIPTION[self.language],
            ),
        )

        self._assert_list_of_strings(
            self._find_element_by_id(
                experiences[0], test_view_constants.MODAL_EXPERIENCE_TECHNOLOGIES_ID_TEMPLATE.format(id=2)
            ),
            [
                test_view_constants.TECHNOLOGY_1[self.language],
                test_view_constants.TECHNOLOGY_2[self.language],
                test_view_constants.TECHNOLOGY_4[self.language],
            ],
        )

        sub_projects_container = self._find_element_by_tag_and_id(
            experiences[0],
            HtmlTag.DIV,
            test_view_constants.SUBPROJECTS_ID_TEMPLATE.format(experience_id=2),
        )

        self._assert_text_of_element(
            sub_projects_container,
            HtmlTag.H4,
            test_view_constants.SUBPROJECTS_TITLE_ID_TEMPLATE.format(experience_id=2),
            test_view_constants.SUBPROJECTS_TITLE[self.language],
        )

        sub_projects = sub_projects_container.find_all(HtmlTag.DETAILS)

        self.assertEqual(
            number_of_sub_projects := len(sub_projects),
            test_view_constants.EXPECTED_NUMBER_OF_SUBPROJECTS_EXPERIENCE_2,
            f"There should be {test_view_constants.EXPECTED_NUMBER_OF_SUBPROJECTS_EXPERIENCE_2}"
            f" sub-projects, but there are {number_of_sub_projects}",
        )

        self._assert_text_of_elements(
            sub_projects[0],
            ElementText(
                html_tag=HtmlTag.TIME,
                element_id=test_view_constants.SUBPROJECT_PERIOD_ID_TEMPLATE.format(experience_id=2, subproject_id=2),
                expected_text=test_view_constants.SUBPROJECT_2_PERIOD[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.SUBPROJECT_DURATION_ID_TEMPLATE.format(experience_id=2, subproject_id=2),
                expected_text=test_view_constants.SUBPROJECT_2_DURATION[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.H4,
                element_id=test_view_constants.SUBPROJECT_TITLE_ID_TEMPLATE.format(experience_id=2, subproject_id=2),
                expected_text=test_view_constants.SUBPROJECT_2_TITLE[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.SUBPROJECT_DESCRIPTION_ID_TEMPLATE.format(
                    experience_id=2, subproject_id=2
                ),
                expected_text=test_view_constants.SUBPROJECT_2_DESCRIPTION[self.language],
            ),
        )

        # SubProject 2 has no client, so the client element should not exist
        self._assert_element_not_exists(
            sub_projects[0],
            test_view_constants.SUBPROJECT_CLIENT_ID_TEMPLATE.format(experience_id=2, subproject_id=2),
        )

        self._assert_list_of_strings(
            self._find_element_by_id(
                sub_projects[0],
                test_view_constants.SUBPROJECT_TECHNOLOGIES_ID_TEMPLATE.format(experience_id=2, subproject_id=2),
            ),
            [
                test_view_constants.TECHNOLOGY_2[self.language],
            ],
        )

        self._assert_text_of_elements(
            sub_projects[1],
            ElementText(
                html_tag=HtmlTag.TIME,
                element_id=test_view_constants.SUBPROJECT_PERIOD_ID_TEMPLATE.format(experience_id=2, subproject_id=1),
                expected_text=test_view_constants.SUBPROJECT_1_PERIOD[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.SUBPROJECT_DURATION_ID_TEMPLATE.format(experience_id=2, subproject_id=1),
                expected_text=test_view_constants.SUBPROJECT_1_DURATION[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.H4,
                element_id=test_view_constants.SUBPROJECT_TITLE_ID_TEMPLATE.format(experience_id=2, subproject_id=1),
                expected_text=test_view_constants.SUBPROJECT_1_TITLE[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.SUBPROJECT_CLIENT_ID_TEMPLATE.format(experience_id=2, subproject_id=1),
                expected_text=test_view_constants.SUBPROJECT_1_CLIENT,
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.SUBPROJECT_DESCRIPTION_ID_TEMPLATE.format(
                    experience_id=2, subproject_id=1
                ),
                expected_text=test_view_constants.SUBPROJECT_1_DESCRIPTION[self.language],
            ),
        )

        self._assert_list_of_strings(
            self._find_element_by_id(
                sub_projects[1],
                test_view_constants.SUBPROJECT_TECHNOLOGIES_ID_TEMPLATE.format(experience_id=2, subproject_id=1),
            ),
            [
                test_view_constants.TECHNOLOGY_1[self.language],
                test_view_constants.TECHNOLOGY_4[self.language],
            ],
        )

        self._assert_text_of_elements(
            experiences[1],
            ElementText(
                html_tag=HtmlTag.TIME,
                element_id=test_view_constants.EXPERIENCE_PERIOD_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.EXPERIENCE_1_PERIOD[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.EXPERIENCE_DURATION_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.EXPERIENCE_1_DURATION[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.EXPERIENCE_TITLE_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.EXPERIENCE_1_TITLE[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.EXPERIENCE_INSTITUTION_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.EXPERIENCE_1_COMPANY,
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.EXPERIENCE_LOCATION_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.EXPERIENCE_1_LOCATION[self.language],
            ),
        )

        self._assert_list_of_strings(
            self._find_element_by_id(
                experiences[1], test_view_constants.EXPERIENCE_TECHNOLOGIES_ID_TEMPLATE.format(id=1)
            ),
            [test_view_constants.TECHNOLOGY_3[self.language]],
        )

        self._assert_attribute_of_element(
            self._find_element_by_tag_and_id(
                experiences[1],
                HtmlTag.BUTTON,
                test_view_constants.EXPERIENCE_MORE_BUTTON_ID_TEMPLATE.format(id=1),
            ),
            common_constants.ATTR_ONCLICK,
            f"{test_view_constants.EXPERIENCE_MODAL_ID_TEMPLATE.format(id=1)}.showModal()",
        )

        self._assert_text_of_elements(
            self._find_element_by_tag_and_id(
                experiences[1],
                HtmlTag.DIALOG,
                test_view_constants.EXPERIENCE_MODAL_ID_TEMPLATE.format(id=1),
            ),
            ElementText(
                html_tag=HtmlTag.TIME,
                element_id=test_view_constants.MODAL_EXPERIENCE_PERIOD_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.EXPERIENCE_1_PERIOD[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.MODAL_EXPERIENCE_DURATION_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.EXPERIENCE_1_DURATION[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.H3,
                element_id=test_view_constants.MODAL_EXPERIENCE_TITLE_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.EXPERIENCE_1_TITLE[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.MODAL_EXPERIENCE_INSTITUTION_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.EXPERIENCE_1_COMPANY,
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.MODAL_EXPERIENCE_LOCATION_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.EXPERIENCE_1_LOCATION[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.MODAL_EXPERIENCE_DESCRIPTION_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.EXPERIENCE_1_DESCRIPTION[self.language],
            ),
        )

        self._assert_list_of_strings(
            self._find_element_by_id(
                experiences[1], test_view_constants.MODAL_EXPERIENCE_TECHNOLOGIES_ID_TEMPLATE.format(id=1)
            ),
            [test_view_constants.TECHNOLOGY_3[self.language]],
        )

        # Experience 1 has no sub-projects, so the sub-projects element should not exist
        self._assert_element_not_exists(
            experiences[1], test_view_constants.SUBPROJECTS_ID_TEMPLATE.format(experience_id=1)
        )

    def test_education_entries(self) -> None:
        my_career = self._find_element_by_id(self.response_data.soup, test_view_constants.MY_CAREER_ID)

        self._assert_text_of_element(
            my_career,
            HtmlTag.H1,
            test_view_constants.EDUCATION_TITLE_ID,
            test_view_constants.EDUCATION_TITLE[self.language],
        )

        education_entries = self._find_element_by_id(
            my_career, element_id=test_view_constants.EDUCATION_LIST_ID
        ).find_all(HtmlTag.LI)

        self.assertEqual(
            number_of_education_entries := len(education_entries),
            test_view_constants.EXPECTED_NUMBER_OF_EDUCATION_ENTRIES,
            f"There should be {test_view_constants.EXPECTED_NUMBER_OF_EDUCATION_ENTRIES}"
            f" education entries, but there are {number_of_education_entries}",
        )

        self._assert_text_of_elements(
            education_entries[0],
            ElementText(
                html_tag=HtmlTag.TIME,
                element_id=test_view_constants.EDUCATION_PERIOD_ID_TEMPLATE.format(id=2),
                expected_text=test_view_constants.EDUCATION_2_PERIOD[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.EDUCATION_DURATION_ID_TEMPLATE.format(id=2),
                expected_text=test_view_constants.EDUCATION_2_DURATION[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.EDUCATION_TITLE_ID_TEMPLATE.format(id=2),
                expected_text=test_view_constants.EDUCATION_2_TITLE[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.EDUCATION_INSTITUTION_ID_TEMPLATE.format(id=2),
                expected_text=test_view_constants.EDUCATION_2_INSTITUTION,
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.EDUCATION_LOCATION_ID_TEMPLATE.format(id=2),
                expected_text=test_view_constants.EDUCATION_2_LOCATION[self.language],
            ),
        )

        self._assert_attribute_of_element(
            self._find_element_by_tag_and_id(
                education_entries[0],
                HtmlTag.BUTTON,
                test_view_constants.EDUCATION_MORE_BUTTON_ID_TEMPLATE.format(id=2),
            ),
            common_constants.ATTR_ONCLICK,
            f"{test_view_constants.EDUCATION_MODAL_ID_TEMPLATE.format(id=2)}.showModal()",
        )

        self._assert_text_of_elements(
            self._find_element_by_tag_and_id(
                education_entries[0],
                HtmlTag.DIALOG,
                test_view_constants.EDUCATION_MODAL_ID_TEMPLATE.format(id=2),
            ),
            ElementText(
                html_tag=HtmlTag.TIME,
                element_id=test_view_constants.MODAL_EDUCATION_PERIOD_ID_TEMPLATE.format(id=2),
                expected_text=test_view_constants.EDUCATION_2_PERIOD[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.MODAL_EDUCATION_DURATION_ID_TEMPLATE.format(id=2),
                expected_text=test_view_constants.EDUCATION_2_DURATION[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.H3,
                element_id=test_view_constants.MODAL_EDUCATION_TITLE_ID_TEMPLATE.format(id=2),
                expected_text=test_view_constants.EDUCATION_2_TITLE[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.MODAL_EDUCATION_INSTITUTION_ID_TEMPLATE.format(id=2),
                expected_text=test_view_constants.EDUCATION_2_INSTITUTION,
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.MODAL_EDUCATION_LOCATION_ID_TEMPLATE.format(id=2),
                expected_text=test_view_constants.EDUCATION_2_LOCATION[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.MODAL_EDUCATION_DESCRIPTION_ID_TEMPLATE.format(id=2),
                expected_text=test_view_constants.EDUCATION_2_DESCRIPTION[self.language],
            ),
        )

        self._assert_text_of_elements(
            education_entries[1],
            ElementText(
                html_tag=HtmlTag.TIME,
                element_id=test_view_constants.EDUCATION_PERIOD_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.EDUCATION_1_PERIOD[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.EDUCATION_DURATION_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.EDUCATION_1_DURATION[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.EDUCATION_TITLE_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.EDUCATION_1_TITLE[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.EDUCATION_INSTITUTION_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.EDUCATION_1_INSTITUTION,
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.EDUCATION_LOCATION_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.EDUCATION_1_LOCATION[self.language],
            ),
        )

        self._assert_attribute_of_element(
            self._find_element_by_tag_and_id(
                education_entries[1],
                HtmlTag.BUTTON,
                test_view_constants.EDUCATION_MORE_BUTTON_ID_TEMPLATE.format(id=1),
            ),
            common_constants.ATTR_ONCLICK,
            f"{test_view_constants.EDUCATION_MODAL_ID_TEMPLATE.format(id=1)}.showModal()",
        )

        self._assert_text_of_elements(
            self._find_element_by_tag_and_id(
                education_entries[1],
                HtmlTag.DIALOG,
                test_view_constants.EDUCATION_MODAL_ID_TEMPLATE.format(id=1),
            ),
            ElementText(
                html_tag=HtmlTag.TIME,
                element_id=test_view_constants.MODAL_EDUCATION_PERIOD_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.EDUCATION_1_PERIOD[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.MODAL_EDUCATION_DURATION_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.EDUCATION_1_DURATION[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.H3,
                element_id=test_view_constants.MODAL_EDUCATION_TITLE_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.EDUCATION_1_TITLE[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.MODAL_EDUCATION_INSTITUTION_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.EDUCATION_1_INSTITUTION,
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.MODAL_EDUCATION_LOCATION_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.EDUCATION_1_LOCATION[self.language],
            ),
            ElementText(
                html_tag=HtmlTag.DIV,
                element_id=test_view_constants.MODAL_EDUCATION_DESCRIPTION_ID_TEMPLATE.format(id=1),
                expected_text=test_view_constants.EDUCATION_1_DESCRIPTION[self.language],
            ),
        )


class TestMyCareerEnglish(BaseTestMyCareerViewContent):
    language = Language.ENGLISH


class TestMyCareerSpanish(BaseTestMyCareerViewContent):
    language = Language.SPANISH
