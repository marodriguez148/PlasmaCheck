# Integration Test Case

## Part 1

---

## TC: User cannot enter an encounter id from a different user in the medical questionnaire (UI)

### Test Ranking
- Priority: Critical
- Rank: 1

### Description
> Verify the user cannot see a different user's questionnaire answers

### Preconditions
- Two members who have scheduled a Scan and are ready to start the Medical Questionnaire
- Get the encounter id by going to either member's medical questionnaire page and grabbing it from the URL

### Test Steps
1. Log in as the member whose encounter id you did not grab
2. Click on the Start button in the Medical Questionnaire Card
3. Replace the encounter id in the URL with the one you obtained from the other member
4. Press enter to load the new URL

### Expected Result
> Page should automatically log you out after 401 error in the API

---

## TC: API Request returns 401 when entering an encounter id that is not authorized for the member (Bearer token) (API)

### Test Ranking
- Priority: Critical
- Rank: 1

### Description
> Verify when calling `GET https://stage-api.ezra.com/diagnostics/api/medicaldata/forms/mq/submissions/{encounter_id}/detail` and entering an encounter id that does not belong to the member, we get a 401 unauthorized error.

### Preconditions
- Two members who have scheduled a Scan and are ready to start the Medical Questionnaire
- Get the encounter id by going to either member's medical questionnaire page and grabbing it from the URL (or database if I had access)

### Test Steps
1. Get the Bearer token of a member and an encounter id that does not belong to them
2. Replace the encounter_id in the API request to the one collected from a different member
3. Use the Bearer token of the user you are testing with
4. Hit the endpoint

### Expected Result
> You should receive a 401 unauthorized error 

---

## Part 2

### Medical Questionnaire Submission Details
```
curl --request get \
  --url https://stage-api.ezra.com/diagnostics/api/medicaldata/forms/mq/submissions/{encounter_id} \
  --compressed \
  --header 'accept: application/json, text/plain, */*' \
  --header 'accept-encoding: gzip, deflate, br, zstd' \
  --header 'accept-language: en-US,en;q=0.9' \
  --header 'authorization: Bearer {Bearer_token}' \
  --header 'baggage: sentry-environment=stage,sentry-release=2391d0fe5a228afa127b53003b477c8980f7980e,sentry-public_key=dfd2428f9e0d58df5404bed162a34002,sentry-trace_id=b42addb6371d4cda8ec91f14582e5ece,sentry-transaction=Flow,sentry-sampled=true,sentry-sample_rand=0.41806817892637904,sentry-sample_rate=1' \
  --header 'connection: keep-alive' \
  --header 'origin: https://myezra-staging.ezra.com' \
  --header 'referer: https://myezra-staging.ezra.com/' \
  --header 'sec-fetch-dest: empty' \
  --header 'sec-fetch-mode: cors' \
  --header 'sec-fetch-site: same-site' \
  --header 'sentry-trace: b42addb6371d4cda8ec91f14582e5ece-b5f569311bd89662-1' \
  --header 'te: trailers' \
  --header 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:150.0) Gecko/20100101 Firefox/150.0'
```

### Medical Questionnaire Submission Data
```
curl --request get \
  --url https://stage-api.ezra.com/diagnostics/api/medicaldata/forms/mq/submissions/{mqSubmissions[id]}/data \
  --compressed \
  --header 'accept: application/json, text/plain, */*' \
  --header 'accept-encoding: gzip, deflate, br, zstd' \
  --header 'accept-language: en-US,en;q=0.9' \
  --header 'authorization: Bearer {bearer_token}' \
  --header 'baggage: sentry-environment=stage,sentry-release=2391d0fe5a228afa127b53003b477c8980f7980e,sentry-public_key=dfd2428f9e0d58df5404bed162a34002,sentry-trace_id=b42addb6371d4cda8ec91f14582e5ece,sentry-transaction=Flow,sentry-sampled=true,sentry-sample_rand=0.41806817892637904,sentry-sample_rate=1' \
  --header 'connection: keep-alive' \
  --header 'origin: https://myezra-staging.ezra.com' \
  --header 'referer: https://myezra-staging.ezra.com/' \
  --header 'sec-fetch-dest: empty' \
  --header 'sec-fetch-mode: cors' \
  --header 'sec-fetch-site: same-site' \
  --header 'sentry-trace: b42addb6371d4cda8ec91f14582e5ece-92cfe4bfea1ab72d-1' \
  --header 'te: trailers' \
  --header 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:150.0) Gecko/20100101 Firefox/150.0'
```

> There are a couple of endpoints that I found that could leak data if not properly handled. First was the Medical Questionnaire Submission Details API request. In this request, we return the member ID and the questionnaire id, which can prove problematic if you could enter an encounter id from a different member. This leads to the Medical Questionnaire Submission Data API request. In this request if we were to enter the questionnaire id that we received from the previous endpoint we would be able to get the questionnaire data from a different member which poses a huge security risk.

## Part 3

> My first thoughts are to treat security as a test requirement. The first step is getting in the mindset that security of these endpoints are required and not an assumption. Questions like "Which user roles should be able to access this enpoint?" or "What data should this endpoint expose?" should be asked during the testing process. 

> The best way to test this many endpoints would be to automate the api requests. We should be able to have an automation api framework in which we can test hitting the endpoints with different categorized user roles to ensure we get the proper response from each role. These test should also be able to ensure say member A can not access member B's data and vise versa. As well as say a member can not access provider specific api calls. 

> The direct trade off would be having to manage 100 endpoints including the need for any new ones. The maintanence burden is something to consider as new enpoints are added. As the number of tests grows so does the time it takes to run them.

> A potenial risk with this method is only using the happy path to test api request. A common gap are tests that only test 200 codes and not authentication based tests. Another risk is keeping track of updates to existing api calls and new authorization tests that may be generated from data being added or removed.