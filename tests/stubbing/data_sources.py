import pytest
from mockito import unstub, when

from src.datasource.faker_member_data import FakerMemberData


@pytest.fixture
def stub_data_sources(mock_faker_member_data):
    when(FakerMemberData).get_df(...).thenReturn(mock_faker_member_data)
    when(FakerMemberData).generate_csv_file(...).thenReturn(None)

    yield

    unstub()
