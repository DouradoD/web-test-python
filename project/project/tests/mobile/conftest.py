def pytest_bdd_after_scenario(request):
    # Quit the WebDriver instance for the teardown
    driver = request.getfixturevalue('driver')
    driver.quit()
