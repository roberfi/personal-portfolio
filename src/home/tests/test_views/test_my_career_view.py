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
        self._assert_template_is_used("cotton/experience_timeline/index.html")
        self._assert_template_is_used("cotton/base.html")

    def test_json_ld_context_and_structure(self) -> None:
        """Test that JSON-LD has correct context and structure."""
        data = self._get_json_ld_data()

        # Verify @context
        self.assertIn("@context", data)
        self.assertEqual(data["@context"]["@vocab"], "https://schema.org/")
        self.assertEqual(data["@context"]["@language"], self.language)

        # Verify @graph structure
        self.assertIn("@graph", data)
        self.assertIsInstance(data["@graph"], list)

        # Verify counts
        work_items = [item for item in data["@graph"] if item["@type"] == "WorkExperience"]
        edu_items = [item for item in data["@graph"] if item["@type"] == "EducationalOccupationalCredential"]
        self.assertEqual(len(work_items), test_view_constants.EXPECTED_NUMBER_OF_EXPERIENCES)
        self.assertEqual(len(edu_items), test_view_constants.EXPECTED_NUMBER_OF_EDUCATION_ENTRIES)

    def test_json_ld_work_experience_schemas(self) -> None:
        """Test that JSON-LD includes complete WorkExperience schemas."""
        data = self._get_json_ld_data()

        work_items = [item for item in data["@graph"] if item["@type"] == "WorkExperience"]

        # Verify Experience 2 (most recent)
        exp2 = work_items[0]
        self.assertEqual(exp2["name"], test_view_constants.EXPERIENCE_2_TITLE[self.language])
        self.assertEqual(exp2["description"], test_view_constants.EXPERIENCE_2_DESCRIPTION[self.language])
        self.assertEqual(exp2["startDate"], test_view_constants.EXPERIENCE_2_START_DATE.isoformat())
        self.assertNotIn("endDate", exp2)

        self.assertEqual(exp2["location"]["@type"], "Place")
        self.assertEqual(exp2["location"]["name"], test_view_constants.EXPERIENCE_2_LOCATION[self.language])

        self.assertEqual(exp2["employer"]["@type"], "Organization")
        self.assertEqual(exp2["employer"]["name"], test_view_constants.EXPERIENCE_2_COMPANY)

        expected_skills = [
            test_view_constants.TECHNOLOGY_1[self.language],
            test_view_constants.TECHNOLOGY_2[self.language],
            test_view_constants.TECHNOLOGY_4[self.language],
        ]
        self.assertEqual(exp2["skills"], expected_skills)

        # Verify Experience 1 (older)
        exp1 = work_items[1]
        self.assertEqual(exp1["name"], test_view_constants.EXPERIENCE_1_TITLE[self.language])
        self.assertEqual(exp1["description"], test_view_constants.EXPERIENCE_1_DESCRIPTION[self.language])
        self.assertEqual(exp1["startDate"], test_view_constants.EXPERIENCE_1_START_DATE.isoformat())
        self.assertEqual(exp1["endDate"], test_view_constants.EXPERIENCE_1_END_DATE.isoformat())

        self.assertEqual(exp1["location"]["@type"], "Place")
        self.assertEqual(exp1["location"]["name"], test_view_constants.EXPERIENCE_1_LOCATION[self.language])

        self.assertEqual(exp1["employer"]["@type"], "Organization")
        self.assertEqual(exp1["employer"]["name"], test_view_constants.EXPERIENCE_1_COMPANY)

        self.assertEqual(exp1["skills"], [test_view_constants.TECHNOLOGY_3[self.language]])

    def test_json_ld_education_schemas(self) -> None:
        """Test that JSON-LD includes complete EducationalOccupationalCredential schemas."""
        data = self._get_json_ld_data()

        edu_items = [item for item in data["@graph"] if item["@type"] == "EducationalOccupationalCredential"]

        # Verify Education 2 (most recent)
        edu2 = edu_items[0]
        self.assertEqual(edu2["name"], test_view_constants.EDUCATION_2_TITLE[self.language])
        self.assertEqual(edu2["description"], test_view_constants.EDUCATION_2_DESCRIPTION[self.language])
        self.assertEqual(edu2["educationalLevel"], test_view_constants.EDUCATION_2_TITLE[self.language])
        self.assertEqual(edu2["dateCreated"], test_view_constants.EDUCATION_2_START_DATE.isoformat())
        self.assertEqual(edu2["validFrom"], test_view_constants.EDUCATION_2_END_DATE.isoformat())

        self.assertEqual(edu2["recognizedBy"]["@type"], "EducationalOrganization")
        self.assertEqual(edu2["recognizedBy"]["name"], test_view_constants.EDUCATION_2_INSTITUTION)
        self.assertEqual(edu2["recognizedBy"]["location"]["@type"], "Place")
        self.assertEqual(
            edu2["recognizedBy"]["location"]["name"], test_view_constants.EDUCATION_2_LOCATION[self.language]
        )

        # Verify Education 1
        edu1 = edu_items[1]
        self.assertEqual(edu1["name"], test_view_constants.EDUCATION_1_TITLE[self.language])
        self.assertEqual(edu1["description"], test_view_constants.EDUCATION_1_DESCRIPTION[self.language])
        self.assertEqual(edu1["educationalLevel"], test_view_constants.EDUCATION_1_TITLE[self.language])
        self.assertEqual(edu1["dateCreated"], test_view_constants.EDUCATION_1_START_DATE.isoformat())
        self.assertEqual(edu1["validFrom"], test_view_constants.EDUCATION_1_END_DATE.isoformat())

        self.assertEqual(edu1["recognizedBy"]["@type"], "EducationalOrganization")
        self.assertEqual(edu1["recognizedBy"]["name"], test_view_constants.EDUCATION_1_INSTITUTION)
        self.assertEqual(edu1["recognizedBy"]["location"]["@type"], "Place")
        self.assertEqual(
            edu1["recognizedBy"]["location"]["name"], test_view_constants.EDUCATION_1_LOCATION[self.language]
        )

    def test_meta_tags(self) -> None:
        """Test that meta tags have correct values for my-career page."""
        self._assert_text_of_element(
            self._find_element_by_html_tag(self.response_data.soup, HtmlTag.TITLE),
            test_view_constants.MY_CAREER_VIEW_META_TITLE[self.language],
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "name", "description"),
            "content",
            test_view_constants.MY_CAREER_VIEW_META_DESCRIPTION[self.language],
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "name", "keywords"),
            "content",
            ", ".join(
                (
                    *test_view_constants.COMMON_META_KEYWORDS[self.language],
                    *test_view_constants.MY_CAREER_VIEW_META_KEYWORDS[self.language],
                )
            ),
        )

    def test_seo_open_graph_tags(self) -> None:
        """Test that Open Graph tags have correct values for my-career page."""
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "property", "og:title"),
            "content",
            test_view_constants.MY_CAREER_VIEW_META_TITLE[self.language],
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(
                self.response_data.soup, HtmlTag.META, "property", "og:description"
            ),
            "content",
            test_view_constants.MY_CAREER_VIEW_META_DESCRIPTION[self.language],
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "property", "og:image"),
            "content",
            "http://testserver/media/background_preview.jpg",
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "property", "og:url"),
            "content",
            f"http://testserver/{self.language}/my-career/",
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "property", "og:type"),
            "content",
            "profile",
        )

    def test_seo_twitter_card(self) -> None:
        """Test that Twitter card meta tags have correct values."""
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "name", "twitter:card"),
            "content",
            "summary_large_image",
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "name", "twitter:title"),
            "content",
            test_view_constants.MY_CAREER_VIEW_META_TITLE[self.language],
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(
                self.response_data.soup, HtmlTag.META, "name", "twitter:description"
            ),
            "content",
            test_view_constants.MY_CAREER_VIEW_META_DESCRIPTION[self.language],
        )
        self._assert_attribute_of_element(
            self._find_element_by_tag_and_attribute(self.response_data.soup, HtmlTag.META, "name", "twitter:image"),
            "content",
            "http://testserver/media/background_preview.jpg",
        )

    def test_experiences(self) -> None:
        my_career = self._find_element_by_id(self.response_data.soup, test_view_constants.MY_CAREER_ID)

        self._assert_text_of_element_by_tag_and_id(
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

        self._assert_text_of_element_by_tag_and_id(
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

        self._assert_text_of_element_by_tag_and_id(
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
