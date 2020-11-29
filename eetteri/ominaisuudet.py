# -*- coding: utf-8 -*-

from django.db.backends.base.features import BaseDatabaseFeatures


class DatabaseFeatures(BaseDatabaseFeatures):
  ''' Ks. super-toteutus. '''
  # gis_enabled = False
  allows_group_by_lob = False
  # allows_group_by_pk = False
  # allows_group_by_selected_pks = False
  # empty_fetchmany_value = []
  update_can_self_select = False

  # interprets_empty_strings_as_nulls = False
  # supports_nullable_unique_constraints = True
  # supports_partially_nullable_unique_constraints = True
  # supports_deferrable_unique_constraints = False

  # can_use_chunked_reads = True
  can_return_columns_from_insert = True
  can_return_rows_from_bulk_insert = True
  # has_bulk_insert = True
  uses_savepoints = False
  # can_release_savepoints = False

  # related_fields_match_type = False
  allow_sliced_subqueries_with_in = False
  # has_select_for_update = False
  # has_select_for_update_nowait = False
  # has_select_for_update_skip_locked = False
  # has_select_for_update_of = False
  # has_select_for_no_key_update = False
  # select_for_update_of_column = False

  # test_db_allows_multiple_connections = True

  supports_unspecified_pk = True
  supports_forward_references = False
  # truncates_names = False
  # has_real_datatype = False
  supports_subqueries_in_group_by = False
  # has_native_uuid_field = False
  # has_native_duration_field = False
  # supports_temporal_subtraction = False
  # supports_regex_backreferencing = True
  # supports_date_lookup_using_string = True
  # supports_timezones = True
  # has_zoneinfo_database = True

  # requires_explicit_null_ordering_when_grouping = False
  # nulls_order_largest = False
  # supports_order_by_nulls_modifier = True
  # order_by_nulls_first = False

  # max_query_params = None
  # allows_auto_pk_0 = True
  # can_defer_constraint_checks = False
  # supports_mixed_date_datetime_comparisons = True
  # supports_tablespaces = False
  supports_sequence_reset = False
  can_introspect_default = False
  can_introspect_foreign_keys = False
  # introspected_field_types = {...}
  supports_index_column_ordering = False
  # can_introspect_materialized_views = False
  # can_distinct_on_fields = False
  atomic_transactions = False
  # can_rollback_ddl = False
  supports_atomic_references_rename = False
  # supports_combined_alters = False

  # supports_foreign_keys = True
  # can_create_inline_fk = True
  # indexes_foreign_keys = True
  # supports_column_check_constraints = True
  # supports_table_check_constraints = True
  can_introspect_check_constraints = False
  supports_paramstyle_pyformat = False
  # requires_literal_defaults = False

  # connection_persists_old_columns = False
  # closed_cursor_error_class = ProgrammingError

  # has_case_insensitive_like = True
  # bare_select_suffix = ''
  # implied_column_null = False
  supports_select_for_update_with_limit = False
  # greatest_least_ignores_nulls = False
  # can_clone_databases = False
  ignores_table_name_case = True
  # for_update_after_from = False

  supports_select_union = False
  supports_select_intersection = False
  supports_select_difference = False
  # supports_slicing_ordering_in_compound = False
  supports_parentheses_in_compound = False
  # supports_aggregate_filter_clause = False
  # supports_index_on_text_field = True
  # supports_over_clause = False
  # supports_frame_range_fixed_distance = False
  # only_supports_unbounded_with_preceding_and_following = False

  supports_cast_with_precision = False
  # time_cast_precision = 6

  # create_test_procedure_without_params_sql = None
  # create_test_procedure_with_int_param_sql = None
  # supports_callproc_kwargs = False

  # supported_explain_formats = set()
  validates_explain_options = False
  # supports_default_in_lead_lag = True

  supports_ignore_conflicts = False
  # requires_casted_case_in_updates = False
  supports_partial_indexes = False
  supports_functions_in_partial_indexes = False
  # supports_covering_indexes = False
  allows_multiple_constraints_on_same_fields = False
  # supports_boolean_expr_in_select_clause = True
  # supports_json_field = True
  # can_introspect_json_field = True
  # supports_primitives_in_json_field = True
  # has_native_json_field = False
  # has_json_operators = False
  # supports_json_field_contains = True
  # json_key_contains_list_matching_requires_list = False

  # supports_collation_on_charfield = True
  # supports_collation_on_textfield = True
  # supports_non_deterministic_collations = True
  # test_collations = {...}

  supports_explaining_query_execution = False
  supports_transactions = False

  # def allows_group_by_selected_pks_on_model(self, model): ...

  # class DatabaseFeatures
