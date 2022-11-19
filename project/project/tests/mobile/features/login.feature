Feature: Login
  As a registered user in the app
  Marcos would like to sign in to the app
  To access your store at any time

  Background:
    Given that Marcos as an ADM user is in the login screen

  @test_1
  Scenario: Try login with invalid values
    Given he fills the user field with the following "skfnlksdfa" value
    And he fills the pass field with the following "adsfdalkfjl" value
    When he triggers the login option
    Then the message about invalid value should be displayed
