# WDS Treasurer v.2.0

This program was created to help me partially automate the task of filling in Google reimbursement forms for a college debate organization. It's based off [another program](https://github.com/angelinahli/wds-treasurer) I wrote some time ago.

My main objective in writing this program is to help me think more about class hierarchy and general code organization.

## Program overview

Input data:
* Google sheet where each row contains information about a specific reimbursement that a student has requested
* Google sheet where each row contains information about a specific student and their contact information

Output:
* List of forms where each form contains all the information needed to submit a form for one students' reimbursements (with a limit of 5 reimbursements associated with each student).
* Output might be formatted in a more user friendly way - e.g. sent as an email to a specific person or formatted as an html page.

## Technical Overview

### Objects

#### (1) Basic data structures

**Reimbursement**
* Represents one reimbursement.
* Instance attributes:
    * Username (key)
    * Date of reimbursement
    * Name of event that needs to be reimbursed
    * Purpose of the reimbursement (as read in from a google sheet)
    * Amount that needs to be reimbursed
    * Number of individuals this reimbursement is paying for
    * Whether this reimbursement has a receipt
    * Whether this reimbursement has been completed
    * (Optional) Usernames of all individuals this reimbursement is paying for
    * (Optional) Link/s to the receipt/s associated with this reimbursement, if any
    * (Optional) Account this reimbursement will be paid through
    * (Optional) Any notes associated with this reimbursement
    * (Optional) If the reimbursement has been processed, the name of the person who processed this

**User**
* Represents one member of our club (who could potentially have filed a reimbursement).
* Instance attributes:
    * Username ('key')
    * Unit box number
    * Address
    * Student ID

#### (2) Google sheets

**Sheet**
* Represents one google sheet of ordered data (where the sheet is filled with data from the first row of data down).

**RSheet**
* Represents one google sheet full of reimbursement data.

**USheet**
* Represents one google sheet full of user data. (Only used occasionally to update a database of users)

#### (3) Databases

**Database**

#### (4) 

## To do
