# @pytest.fixture
# def mock_function(mocker):
#    mocked_cursor_result = mocker.MagicMock()
#    mocked_cursor_result.mappings.return_value = mocker.MagicMock()
#    mocked_cursor_result.mappings.return_value.all.return_value = [
#        {"total_time": Decimal(123.456)}
#    ]
#    return mocker.patch(
#        "app.analytics.project.total_test_duration.db.session.execute",
#        return_value=mocked_cursor_result,
#    )
