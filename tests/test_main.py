import pytest
import main

def test_add_app():
    """Test that apps can be added correctly to the MultiApp"""
    app = main.MultiApp()
    assert len(app.apps) == 0

    # Add a dummy app and check the number of apps
    def dummy_app():
        pass

    app.add_app("Dummy", dummy_app)
    assert len(app.apps) == 1
    assert app.apps[0]['title'] == "Dummy"
    assert app.apps[0]['function'] == dummy_app

def test_page_title():
    """Test if the page title is set correctly"""
    assert main.st.get_option("page_title") == "DATALASIS"
