INSERT INTO `rmcs-project`.accountable_forms_afprefix (id, name) VALUES ('PREFIX_REQUEST', 'RIS');
INSERT INTO `rmcs-project`.accountable_forms_afprefix (id, name) VALUES ('PREFIX_TRANSACTION', 'IRAF');

INSERT INTO `rmcs-project`.accountable_forms_afstate (id, name) VALUES ('STATE_ISSUED', 'ISSUED');
INSERT INTO `rmcs-project`.accountable_forms_afstate (id, name) VALUES ('STATE_OPEN', 'OPEN');

INSERT INTO `rmcs-project`.accounts_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, id, tnxCode)
 VALUES ('pbkdf2_sha256$320000$OGh5heKXNgAB21atgc92Hm$0QeGfRDCRIhVtvMOIGphE/PCl0wyV2/k7b03rQHoBhc=', '2022-03-15 12:57:33.582670', 1, 'admin', '', '', 'admin@email.com', 1, 1, '2022-03-15 12:56:09.061064', '0e724192fa8440fc92de922b662d24f8', '');

INSERT INTO `rmcs-project`.accountable_forms_aftransactiontype (id, name) VALUES ('TYPE_ISSUANCE', 'ISSUANCE');
INSERT INTO `rmcs-project`.accountable_forms_aftransactiontype (id, name) VALUES ('TYPE_PURCHASE', 'PURCHASE');

INSERT INTO `rmcs-project`.accountable_forms_aftransactionstatus (id, name) VALUES ('STATUS_PENDING', 'PENDING');
INSERT INTO `rmcs-project`.accountable_forms_aftransactionstatus (id, name) VALUES ('STATUS_CANCELLED', 'CANCELLED');
INSERT INTO `rmcs-project`.accountable_forms_aftransactionstatus (id, name) VALUES ('STATUS_COMPLETED', 'COMPLETED');


INSERT INTO `rmcs-project`.accountable_forms_aftype (form_number, title, series_length, use_type, unit, quantity) VALUES (51, 'ACCOUNTABLE FORM', 7, null, 'STUB', 1);
