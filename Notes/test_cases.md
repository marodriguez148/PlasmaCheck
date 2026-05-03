# Question 1

# Test Cases
---

## TC-1: Select Plan Page Loads and Verify Page elements (Select Plan Page)

### Test Ranking
- Priority: Critial
- Rank: 1

### Description
> Verify that the Select Plan page loads with all the proper web elements

### Preconditions
- Logged in to a member account and click on the "Book a Scan" button
- Or Sign up as a new member and follow the sign up process

### Test Steps
1. Verify that all loading bars or loading elements have disappeared
2. Url should contain `/select-plan`
3. Encounter cards with scan selections are visible
4. Verify the Cancel button appears
5. Verify that the continue button appears but is disabled

### Expected Result
> The page should load and all expected page elements appear

---

## TC-2: Schedule Scan page loads and Verify Page elements (Schedule Scan Page)

### Test Ranking
- Priority: Critical
- Rank: 1

### Description
> Verify that the Schedule Scan page loads with all the proper web elements

### Preconditions
- Logged in to a member account
- Or Sign up as a new member and follow the sign up process
- Member has navigated to the Schedule Scan page from the previous booking page

### Test Steps
1. Verify that all loading bars or loading elements have disappeared
2. Url should contain `/schedule-scan`
3. Location cards are visible
4. Verify the Back button appears
5. Verify that the continue button appears but is disabled

### Expected Result
> The page should load and all expected page elements appear

---

## TC-3: Reserve Appointment page loads and Verify Page elements (Reserve Appointment Page)

### Test Ranking
- Priority: Critical
- Rank: 1

### Description
> Verify that the Reserve Appointment page loads with all the proper web elements

### Preconditions
- Logged in to a member account
- Or Sign up as a new member and follow the sign up process
- Member has navigated to the Reserve Appointment page from the previous booking page

### Test Steps
1. Verify that all loading bars or loading elements have disappeared
2. Url should contain `reserve-appointment`
3. The Payment Accordion is visible
4. Verify the Card Accordion is open while the other (Bank, Affirm) are closed
5. Verify the Back button appears
6. Verify that the continue button appears but is disabled

### Expected Result
> The page should load and all expected page elements appear

---

## TC-4: Scan Confirm page loads and Verify Page elements (Scan Confirm Page)

### Test Ranking
- Priority: Critical
- Rank: 1

### Description
> Verify that the Reserve Appointment page loads with all the proper web elements

### Preconditions
- Logged in to a member account
- Or Sign up as a new member and follow the sign up process
- Member has navigated to the Scan Confirm page from the previous booking page

### Test Steps
1. Verify that all loading bars or loading elements have disappeared
2. Url should contain `/scan-confirm`
3. The Begin Medical Questionnaire button is visible
4. Verify Scan Details card is visible
5. Verify the Go to Dashboard link button appears

### Expected Result
> The page should load and all expected page elements appear

---

## TC-5: Advancing to the Schedule Scan Page (Select Plan Page)

### Test Ranking
- Priority: Critical
- Rank: 2

### Description
> Verify that the user can advance to the next step of the booking process

### Preconditions
- Logged in to a member account
- Or Sign up as a new member and follow the sign up process
- Member has navigated to the Select Plans page
- Member has selected a Scan

### Test Steps
1. Click the continue button
2. Verify that all loading elements have disappeared
3. Verify the browser has brought you to the Schedule Scan page

### Expected Result
> The Schedule Scan page has loaded

---


## TC-6: Advancing to the Reserve Appointment step (Schedule Scan Page)

### Test Ranking
- Priority: Critical
- Rank: 2

### Description
> Verify that the user can advance to the next step of the booking process

### Preconditions
- Logged in to a member account
- Or Sign up as a new member and follow the sign up process
- Member has navigated to the Schedule Scan page
- Member has selected a Location
- Member has selected a date and time

### Test Steps
1. Click the continue button
2. Verify that all loading elements have disappeared
3. Verify the browser has brought you to the Reserve Appointment page

### Expected Result
> The Reserve Appointment page has loaded

---

## TC-7: Advancing to the Scan Confirm step (Reserve Appointment Page) 

### Test Ranking
- Priority: Critical
- Rank: 2

### Description
> Verify that the user can advance to the next step of the booking process

### Preconditions
- Logged in to a member account
- Or Sign up as a new member and follow the sign up process
- Member has navigated to the Reserve Appointment page
- Member has entered their card information

### Test Steps
1. Click the continue button
2. Verify that all loading elements have disappeared
3. Verify the browser has brought you to the Scan Confirm page

### Expected Result
> The Scan Confirm page has loaded

---

## TC-8: Enter Card info into input form (Reserve Appointment Page)

### Test Ranking
- Priority: High
- Rank: 3

### Description
> Verify entering info into the card input form

### Preconditions
- Logged in to a member account
- Or Sign up as a new member and follow the sign up process
- Member has navigated to the Reserve Appointment page from the previous booking page
- Test Card Credentials to enter into the form

### Test Steps
1. Enter the Card Number
2. Enter the Expiration Date
3. Enter the Security Code
4. Select a Country from the dropdown
5. Enter the Zip Code
6. Verify the Continue button has been enabled

### Expected Result
> The continue button has been enabled and the user is ready to advance to the next step

---

## TC-9: Accordian Navigation (Reserve Appointment Page)

### Test Ranking
- Priority: High
- Rank: 4

### Description
> Verify you can navigate between the different accordion sections

### Preconditions
- Logged in to a member account
- Or Sign up as a new member and follow the sign up process
- Member has navigated to the Reserve Appointment page from the previous booking page

### Test Steps
1. Confirm the Card Accordion is expanded
2. Verify all the form inputs
    - Card Number text input
    - Expiration Date text input
    - Security Code input
    - Country dropdown
    - zip code input
        - Optional info
            - email input
            - mobile number input
3. Click on the Bank Accordion
4. Verify the Card Accordion has collapsed and the Bank Accordion has expanded
5. Verify the form inputs
    - Bank Search text input
    - Bank list selector
6. Click on the Affirm accordion
7. Verify Bank Accordion has collapsed and the Affirm Accordion has expanded
8. Verify the Affirm description

### Expected Result
> Verify the user can navigate through the different accordians and their form inputs are displayed

---

## TC-10: Selecting a Scan (Select Plan Page)

### Test Ranking
- Priority: High
- Rank: 5

### Description
> Verify selecting a scan 

### Preconditions
- Logged in to a member account and click on the "Book a Scan" button
- Or Sign up as a new member and follow the sign up process

### Test Steps
1. Select Any Scan from the list of Scan Encounter cards
2. The Page should auto-scroll to the bottom
3. Addon card appears with the selected Scan's info
4. Verify that the Continue button is now enabled

### Expected Result
> The page auto scrolls to the bottom of the page, displays an Addon card with the selected plan info, and the continue button is enabled.

---

## TC-11: Selecting a Location card (Schedule Scan Page)

### Test Ranking
- Priority: High
- Rank: 5

### Description
> Verify you can select a location from the displayed list

### Preconditions
- Logged in to a member account
- Or Sign up as a new member and follow the sign up process
- Member has navigated to the Schedule Scan page from the previous booking page

### Test Steps
1. Click on any of the location cards
2. Verify all loading elements have disappeared
3. Verify the page auto-scrolls to the bottom
4. Verify the Calendar date selector has appeared

### Expected Result
> Page auto scrolls to the bottom and the Calendar Date selector is displayed

---

## TC-12: Entering a date and time for the scan (Schedule Scan Page)

### Test Ranking
- Priority: High
- Rank: 5

### Description
> Verify selecting a date and time for the scan

### Preconditions
- Logged in to a member account
- Or Sign up as a new member and follow the sign up process
- Member has navigated to the Schedule Scan page from the previous booking page
- Member has selected a location

### Test Steps
1. Click on the month dropdown
2. Select a month in the present/future
3. Click on a date that is not disabled
4. Verify a list of times have appeared to select from
5. Click on any time from the list
6. Verify the Continue button has been enabled

### Expected Result
> The selected date and time have been highlighted and the continue button is enabled

---

## TC-13: Encounter cards display the correct infomation (Select Plan Page)

### Test Ranking
- Priority: Medium
- Rank: 6

### Description
> Verify that the scan selection encounter cards display the correct information

### Preconditions
- Logged in to a member account and clicking on the "Book a Scan" button
- Or Sign up as a new member and follow the sign up process

### Test Steps
1. Verify the Scan Name title for each Scan option is displayed and correct
2. Verify the Payment info is displayed and correct
3. Verify the Payment method description is displayed and correct
4. Verify the Scan Description is displayed and correct
5. Verify the What's included section is displayed and correct

### Expected Result
> All the information for each scan encounter card is correct

---

## TC-14: Addon Cards display the correct information (Select Plan Page)

### Test Ranking
- Priority: Medium
- Rank: 6

### Description
> Verify that the Scan Addon cards display the correct information

### Preconditions
- Logged in to a member account
- Or Sign up as a new member and follow the sign up process
- Member has navigated to the Select Plans page
- Member has selected a Scan

### Test Steps
1. Verify the Addon Card Title displays the Scan Name
2. Verify the short scan description
3. Verify the scan price
4. Verify the longer Scan description
5. Verify the What's Included section

### Expected Result
> The Addon Card displays the correct information for the scan selected

---

## TC-15: Location cards appear and have the correct info (Schedule Scan Page)

### Test Ranking
- Priority: Medium
- Rank: 6

### Description
> Verify the list of location cards and that they have the correct info

### Preconditions
- Logged in to a member account
- Or Sign up as a new member and follow the sign up process
- Member has navigated to the Schedule Scan page from the previous booking page

### Test Steps
1. Verify the Suggesting Pill for qualifying locations
2. Verify the location name is displayed and correct
3. Verify the location address is displayed and correct
4. Verify the View on Map link button is displayed and correct

### Expected Result
> All location info is displayed and correct for each location card

---

## Top 3 test cases and why

> The first four test cases are considered the most important because they ensure that the core pages of the booking process load correctly with all essential elements. If these pages fail to load, users cannot proceed through the appointment booking workflow, resulting in a critical disruption to the business's ability to facilitate appointments.

> Test Cases 5 through 7 are ranked as the second most important because they validate the end-to-end flow of the booking process. These tests confirm that user inputs from earlier steps are properly propagated and affect the content displayed on subsequent pages, ensuring a cohesive user experience—for instance, selecting a specific scan type may limit available locations and time slots.

> The last Important test case is test case 8 because it validates a critical component of the booking workflow, which is the ability to securely input and process payment information. Payment handling is the next essential step for completing transactions. If users cannot enter valid card details or if the form fails to enable progression, the entire booking process stalls at the payment stage, preventing revenue generation and potentially causing user frustration or abandonment.