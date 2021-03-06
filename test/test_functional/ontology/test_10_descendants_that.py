def test_dt_no_restrictions(target_list_track):
    assert set(target_list_track.descendants_that()) == {
        "outside_list_primitive",
        "target_folder_outer",
        "target_folder_inner",
        "target_list",
        "target_list_name",
        "target_list_color",
        "target_keyed_list",
        "target_keyed_list_color"
    }

def test_dt_restrict_data_type(target_list_track):
    assert set(target_list_track.descendants_that(data_type="Text")) == {
        "target_list_name",
        "target_list_color",
        "target_keyed_list_color"
    }

def test_dt_primitive_inside_list(target_list_track):
    assert set(target_list_track.descendants_that(container=-1, inside_list=1)) == {
        "target_list_name",
        "target_list_color",
        "target_keyed_list_color"
    }

def test_dt_primitive_outside_list(target_list_track):
    assert set(target_list_track.descendants_that(container=-1, inside_list=-1)) == {
        "outside_list_primitive"
    }

def test_dt_primitive(target_list_track):
    assert set(target_list_track.descendants_that(container=-1)) == {
        "target_list_name",
        "target_list_color",
        "target_keyed_list_color",
        "outside_list_primitive"
    }

def test_dt_require_container(target_list_track):
    assert set(target_list_track.descendants_that(container=1)) == {
        "target_folder_outer",
        "target_folder_inner",
        "target_list",
        "target_keyed_list",
    }

def test_dt_require_specific_container(target_list_track):
    assert set(target_list_track.descendants_that(container=1, data_type="Folder")) == {
        "target_folder_outer",
        "target_folder_inner"
    }

def test_dt_require_specific_primitive(target_list_track):
    assert set(target_list_track.descendants_that(container=-1, data_type="Text")) == {
        "target_list_name",
        "target_list_color",
        "target_keyed_list_color"
    }

def test_dt_require_container_contradiction(target_list_track):
    assert set(target_list_track.descendants_that(container=1, data_type="Text")) == set()

def test_dt_require_primitive_contradiction(target_list_track):
    assert set(target_list_track.descendants_that(container=-1, data_type="Folder")) == set()
