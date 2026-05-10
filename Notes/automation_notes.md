# Automation Notes

### Initial thoughts
- Using python with playwright, most accustomed to python and easier to read
- Will most likely build automation test for Login and running through the booking flow
    - Login should be easy to test stability of automation test
    - Automating the Booking flow should prove I can write an end to end test (Mostly with out a DB)
- Unsure if I have time to build out component code but will try
- I wonder if I will have enough time for api test?

### Current thoughts and iteration notes
- Use claude to build pytest commandline interface and logger to quickly get to writing test automation
- Build out base page that will use the driver to create a baseline of methods used in all pages
- All pages will inherit from login which inherts from base_page
    - I don't know if I like that instead of just logging in with the base page. Will test it out
- If I have time I would love to create wait functions. Default playwright locator checkers are way too fast
- Logger isn't logging anything past initial start to tests. Neet to investigate
- I need to get better at creating logs, man I suck at it even with AI
- don't like some of the methods claude gave me for base_component. I don't like `self.root.locator...`, maybe I need to understand playwright more
- Want to generalize the dropdown component so I can use it with the states dropdown
- Using pytest.main for better log output
- I wonder how to get a bearer token from an already logged in user
- Wish I had DB access to get locator and location info


### Booking test notes
- Kinda hard to try and test each page individually, this is going to have to be a End to end test
    - Verify elements when on each page
    - Verify moving through the flow
- I doubt I'll have time but would love to link sign up to booking flow as well
- I really need to figure out how to get the bearer token once already logged in
- creating accordian component
- should probably add a component for the breadcrumb navigation, if I have time
- Accordion selectors are so infuriating. Working with iframes are hard
    - I hate Accordions now T_T
- Now that booking flow is complete I'm hoping to see if I can automate api requests in the time I have left


### Provider page
- Doubt I will have time for this
- If I do maybe just make a login test
- Hard to test anything there without DB data

### API tests
- Got bearer token
- Doing get licenced states to test out api tests
- Need to find out where to get encounter ids and package ids
    - Can make an encounter id in the bookingscan request but not sure how to get an existing one
