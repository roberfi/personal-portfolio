from __future__ import annotations

from typing import TYPE_CHECKING, ContextManager
from unittest.mock import patch

import home.tests.test_views.utils.constants as test_view_constants
from home.models import Education, Experience, PersonalInfo, SubProject, Technology
from utils.test_utils.base_view_test_case import BaseViewTestCase
from utils.test_utils.constants import Language
from utils.test_utils.mocks import get_date_with_mocked_today

if TYPE_CHECKING:
    from datetime import date


class BaseHomeViewTest(BaseViewTestCase):
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
