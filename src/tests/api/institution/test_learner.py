#  Copyright (c) 2021 Mireia Bellot
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU Affero General Public License as
#      published by the Free Software Foundation, either version 3 of the
#      License, or (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU Affero General Public License for more details.
#
#      You should have received a copy of the GNU Affero General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
""" Test module for institution management """
import logging

import pytest

import tests.utils

from tests.utils import getting_variables


@pytest.mark.django_db
def test_api_institution_learner(rest_api_client, user_global_admin, institution_course_test_case):
    """

    INSTITUTION TEST: LEARNER
       1) List learners
       2) Create a new learner
       3) Read new learner information
       4) Update new learner
       5) Accept an informed consent for a learner
       6) Reject current Informed Consent of a learner
       7) Read SEND categories assigned to a learner
       8) Add SEND category to a learner
       9) Remove a SEND Category from a learner
       10) Delete new learner
    """
    pytest.skip("TODO: Adapt to the change from learner to user endpoints")

    institution_user = institution_course_test_case['user'].institutionuser
    institution_id = institution_course_test_case['institution'].id
    learner = institution_course_test_case['learner']
    learner_user = learner.institutionuser
    instructor_user = institution_course_test_case['instructor'].institutionuser

    # 666?
    # Global Administration privileges
    # user_global_admin.is_staff = True
    # user_global_admin.save()

    # Set global admin user.
    # rest_api_client.force_authenticate(user=user_global_admin)

    logging.info('\nTESTING INSTITUTIONS: Learners *********************************************')

    # Get the list of Institutions
    """ ---------------------------------------------------------------------
    LIST LEARNERS:
       GET /api/v2/institution/(int: institution_id)/learner/
       Status Codes:
           200 OK – Ok
           404 Not Found – Institution not found
    Request Headers: Authorization - JWT with Institution Admin/Instructor privileges
    """
    logging.info('\n1) LIST LEARNERS --------------------------------------')
    # institution_user.legal_admin = False
    # institution_user.save()
    # rest_api_client.force_authenticate(user=institution_user)
    instructor_user.legal_admin = False
    instructor_user.save()
    rest_api_client.force_authenticate(user=instructor_user)

    str_path = '/api/v2/institution/{}/learner/'.format(institution_id)
    str_message = 'RESPONSE institution_id:{}'.format(institution_id)
    body = tests.utils.get_rest_api_client(rest_api_client, str_path,
                                           'List learners', str_message, 200)
    n_learners = body['count']
    variables = getting_variables(body, institution_id)

    if variables['n_institution'] > 0:
        tests.utils.check_pagination(rest_api_client, body)
        args = [['List Learners'], ['ID FIRST LEARNER: ', variables['id_first_institution']],
                ['NUMBER OF LEARNERS:', variables['n_institution']],
                ['INSTITUTION ID TEST', institution_id],
                ['ID NON EXISTING INSTITUTION:', variables['id_non_existing_institution']]]
    else:
        args = [['List Institutions'], ['Empty Institutions list. Reading first Institution test will be skipped.']]

    tests.utils.print_log(args)

    # 2) Create a new learner
    """ ---------------------------------------------------------------------
    CREATE A NEW LEARNER:
        POST /api/v2/institution/(int:institution_id)/learner/
        Request JSON Object
            uid (string) – Unique ID of this learner in the institution.
            email (string) – Email of the learner. If institution mail_domain is provided, 
                             this email must be in this domain.
            first_name (string) – First name of the learner.
            last_name (string) – Last name of the learner.
        Status Codes:
            201 Created – Created
            400 Bad Request – Invalid information provided. The response contains the description of the errors.
            404 Not Found – Institution not found
    Request Headers: Authorization - JWT with Institution Admin privileges
    """
    # 666? why instructor user works if it does not have admin privileges?
    # 666? It works properly with "legal_admin = False"
    instructor_user.legal_admin = True
    instructor_user.save()
    rest_api_client.force_authenticate(user=instructor_user)

    logging.info('\n2) CREATE A NEW LEARNER --------------------------------------')
    str_data = {'uid': 'LEARNER_UID', 'email': 'mail_test@tesla-ce.eu',
                'first_name': 'TEST_LEARNER_NAME',
                'last_name': 'TEST_LEARNER_LASTNAME'}
    new_learner_id = tests.utils.post_rest_api_client(rest_api_client, str_path, str_data,
                                                      'Create a new learner', 'RESPONSE: ', 201)

    #  # Ensure number of learners has increased
    body = tests.utils.get_rest_api_client(rest_api_client, str_path,
                                           'List learners', 'RESPONSE:', 200)
    assert n_learners + 1 == body['count']

    # TODO? Create a new learner errors
    # Status 400: Validate unique email
    error_new_learner = tests.utils.post_rest_api_client(rest_api_client, str_path,
                                                         str_data,
                                                         'Create a new learner failed',
                                                         'RESPONSE: ', 400)

    # 3) Read learner information
    """ ---------------------------------------------------------------------
    READ LEARNER INFORMATION:
    GET /api/v2/institution/(int: institution_id)/learner/(int: learner_id)/
    Status Codes:
        200 OK – Ok
        404 Not Found – Institution not found
        404 Not Found – Learner not found
    Privileges: Institution Admin/Instructor privileges
    """
    logging.info('\n3) READ LEARNER INFORMATION --------------------------------------')
    instructor_user.legal_admin = False
    instructor_user.save()
    rest_api_client.force_authenticate(user=instructor_user)

    str_path = '/api/v2/institution/{}/learner/{}/'.format(institution_id, new_learner_id)
    str_response = 'RESPONSE Learner ID={}:'.format(new_learner_id)
    body = tests.utils.get_rest_api_client(rest_api_client, str_path,
                                           'Read Learner Information', str_response, 200)
    # No informed consent for a new learner
    assert body['consent'] is None
    assert body['consent_rejected'] is None
    # No SEND category for a new learner
    assert body['send']['is_send'] is False


    # TODO? Read Learner information errors

    # 4) Update learner
    """ ---------------------------------------------------------------------
    UPDATE LEARNER:
        PUT /api/v2/institution/(int: institution_id)/learner/(int: learner_id)/
        Status Codes:
            200 OK – Ok
            400 Bad Request – Invalid information provided. The response contains the description of the errors.
            404 Not Found – Institution not found
            404 Not Found – Learner not found
    Request Headers: Authorization - JWT with Institution Admin privileges
    """
    logging.info('\n4) UPDATE LEARNER --------------------------------------')
    institution_user.legal_admin = True
    institution_user.save()
    rest_api_client.force_authenticate(user=institution_user)

    str_data = {'uid': 'LEARNER_UID_UPDATED', 'email': 'mail_test_UPDATED@tesla-ce.eu',
                'first_name': 'TEST_LEARNER_NAME_UPDATED',
                'last_name': 'TEST_LEARNER_LASTNAME_UDPATED'}
    tests.utils.put_rest_api_client(rest_api_client, str_path, str_data,
                                    'Update Learner', 'RESPONSE: ', 200)

    # TODO? Update Learner errors

    # 5) Accept an informed consent for a learner
    """ ---------------------------------------------------------------------
    ACCEPT INFORMED CONSENT FOR A LEARNER:
        POST /api/v2/institution/(int: institution_id)/user/(int: learner_id)/ic/
        Request JSON Object: version (string) – Informed consent version to assign
        Status Codes:
            200 OK – Ok
            400 Bad Request – Invalid information provided. The response contains the description of the errors.
            400 Not Found – Institution not found
            404 Not Found – Learner not found
    Request Headers: Authorization - JWT with Institution Admin privileges
    """
    logging.info('\n5) ACCEPT INFORMED CONSENT FOR A LEARNER --------------------------------------')
    # Getting valid informed consent for current institution
    ic_str_path = '/api/v2/institution/{}/ic/'.format(institution_id)
    ic_str_response = 'RESPONSE institution_id={}:'.format(institution_id)
    ic_body = tests.utils.get_rest_api_client(rest_api_client, ic_str_path,
                                              'List Informed Consents', ic_str_response, 200)

    # If no valid informed consent exist: create one
    if ic_body['count'] > 0:
        ic_version = ic_body['results'][0].version
        str_path = '/api/v2/institution/{}/user/{}/ic'.format(institution_id, new_learner_id)
        str_data = {'version': ic_version}
        tests.utils.post_rest_api_client(rest_api_client, str_path, str_data,
                                         'Accept Informed Consent for a Learner',
                                         'RESPONSE: ', 200)
    # If valid informed consent exist
    else:
        str_path = '/api/v2/institution/{}/ic/'.format(institution_id)
        str_data = {'version': '0.0.1', 'valid_from': '2021-06-01T10:00'}
        new_ic_id = tests.utils.post_rest_api_client(rest_api_client, str_path,
                                                     str_data, 'Create a new Informed Consent',
                                                     'RESPONSE:', 201)
        str_path = '/api/v2/institution/{}/learner/{}/ic/'.format(institution_id, new_learner_id)
        str_data = {'version': '0.0.1'}
        tests.utils.post_rest_api_client(rest_api_client, str_path, str_data,
                                         'Accept Informed Consent for a Learner',
                                         'RESPONSE: ', 200)

    str_path = '/api/v2/institution/{}/user/{}/'.format(institution_id, new_learner_id)
    str_response = 'RESPONSE Learner ID={}:'.format(new_learner_id)
    body = tests.utils.get_rest_api_client(rest_api_client, str_path,
                                           'Read Learner Information', str_response, 200)
    assert body['consent'] is not None

    # 6) Reject current Informed Consent of a learner
    """ ---------------------------------------------------------------------
    REJECT CURRENT INFORMED CONSENT OF A LEARNER:
        DELETE /api/v2/institution/(int: institution_id)/user/(int: learner_id)/ic/
        Status Codes:
            200 OK – Ok
            400 Bad Request – Invalid information provided. The response contains the description of the errors.
            400 Not Found – Institution not found
            404 Not Found – Learner not found
    Request Headers: Authorization - JWT with Institution Admin privileges
    """
    logging.info('\n6) REJECT INFORMED CONSENT FOR A LEARNER --------------------------------------')
    str_path = '/api/v2/institution/{}/user/{}/ic/'.format(institution_id, new_learner_id)
    tests.utils.delete_rest_api_client(rest_api_client, str_path,
                                       'Reject Current Informed Consent of a Learner', "RESPONSE: ", 200)

    str_path = '/api/v2/institution/{}/user/{}/'.format(institution_id, new_learner_id)
    str_response = 'RESPONSE Learner ID={}:'.format(new_learner_id)
    body = tests.utils.get_rest_api_client(rest_api_client, str_path,
                                           'Read Learner Information', str_response, 200)
    assert body['consent_rejected'] is not None



    # 7) Read SEND categories assigned to a learner
    """ ---------------------------------------------------------------------
    Read SEND categories assigned to a learner:
        GET /api/v2/institution/(int: institution_id)/learner/(int: learner_id)/send/
        Status Codes:
            200 OK – Ok
            400 Bad Request – Invalid information provided. The response contains the description of the errors.
            404 Not Found – Institution not found
            404 Not Found – Learner not found
    Request Headers: Authorization - JWT with Institution Admin/SEND privileges
    """
    logging.info('\n7) Read SEND categories assigned to a learner --------------------------------------')
    instructor_user.send_admin = True
    instructor_user.save()
    rest_api_client.force_authenticate(user=instructor_user)

    str_path = '/api/v2/institution/{}/learner/{}/send/'.format(institution_id, new_learner_id)
    str_response = 'RESPONSE Learner ID={}:'.format(new_learner_id)
    body = tests.utils.get_rest_api_client(rest_api_client, str_path,
                                           'Read SEND categories assigned to a learner',
                                           str_response, 200)
    # No SEND category for a new learner
    assert body['count'] == 0


    # 8) Add SEND category to a learner
    """ ---------------------------------------------------------------------
    Add SEND category to a learner:
        POST /api/v2/institution/(int: institution_id)/learner/(int: learner_id)/send/
        Request JSON Object:
            category (int) – SEND Category ID
            expires_at (datetime) – When the special need is temporal, provide the date when it disappears. For permanent needs, let it null.
        Status Codes:
            200 OK – Ok
            400 Bad Request – Invalid information provided. The response contains the description of the errors.
            404 Not Found – Institution not found
            404 Not Found – Learner not found
            404 Not Found – SEND Category not found
    Request Headers: Authorization - JWT with Institution Admin/SEND privileges
    """
    '''
    logging.info('\n8) Add SEND category to a learner --------------------------------------')
    str_path = '/api/v2/institution/{}/learner/{}/send/'.format(institution_id, new_learner_id)
    tests.utils.post_rest_api_client(rest_api_client, str_path, str_data,
                                     'Add SEND category to a learner',
                                     'RESPONSE: ', 200)
    # 666 add getting list of available categories ID
    str_data = {'category': 1}
    new_send_id = tests.utils.post_rest_api_client(rest_api_client, str_path, str_data,
                                                   'Add SEND category to a learner', 'RESPONSE: ', 200)
    '''

    # 9) Remove a SEND Category from a learner
    """ ---------------------------------------------------------------------
    Remove a SEND Category from a learner:
        DELETE /api/v2/institution/(int: institution_id)/learner/(int: learner_id)/send/(int: send_assig_id)/
        Status Codes:
            200 OK – Ok
            400 Bad Request – Invalid information provided. The response contains the description of the errors.
            404 Not Found – Institution not found
            404 Not Found – Learner not found
            404 Not Found – SEND Category not found
    Request Headers: Authorization - JWT with Institution Admin/SEND privileges
    """

    # 10) Delete learner
    """ ---------------------------------------------------------------------
    DELETE LEARNER:
        DELETE /api/v2/institution/(int: institution_id)/learner/(int: learner_id)/
        Status Codes:
            200 OK – Ok
            400 Bad Request – Invalid information provided. The response contains the description of the errors.
            404 Not Found – Institution not found
            404 Not Found – Learner not found
    Request Headers: Authorization - JWT with Institution Admin/Legal privileges
    """
    logging.info('\n10) DELETE LEARNER --------------------------------------')

    str_path = '/api/v2/institution/{}/learner/{}/'.format(institution_id, new_learner_id)
    tests.utils.delete_rest_api_client(rest_api_client, str_path,
                                       'Delete Learner', "RESPONSE: ", 204)

    # Ensure number of learners has decreased
    str_path = '/api/v2/institution/{}/learner/'.format(institution_id)
    str_message = 'RESPONSE institution_id:{}'.format(institution_id)
    body = tests.utils.get_rest_api_client(rest_api_client, str_path,
                                           'List learners', str_message, 200)
    assert body['count'] == n_learners

    # TODO? Delete learner errors

    # pytest.skip("TODO")
