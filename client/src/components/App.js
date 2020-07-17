import React from "react";
import { Router, Route, Switch } from "react-router-dom";

import Home from "./Home";
import FlowCreate from "./flows/FlowCreate";
import FlowEdit from "./flows/FlowEdit";
import FlowDelete from "./flows/FlowDelete";
import FlowList from "./flows/FlowList";
import FlowShow from "./flows/FlowShow";
import SignUp from "./auth/SignUp";
import LogIn from "./auth/LogIn";
import LogOut from "./auth/LogOut";
import Header from "./Header";
import Visualization from "./visualizations/Visualization";

import history from "../history";

const App = () => {
    return (
        <Router history={history}>
            <div>
                <Header />
                <Switch>
                    <Route path="/" exact component={Home} />
                    <Route path="/signup" exact component={SignUp} />
                    <Route path="/login" exact component={LogIn} />
                    <Route path="/logout" exact component={LogOut} />
                    <Route path="/flows" exact component={FlowList} />
                    <Route path="/flows/create" exact component={FlowCreate} />
                    <Route path="/flows/edit/:id" exact component={FlowEdit} />
                    <Route
                        path="/flows/delete/:id"
                        exact
                        component={FlowDelete}
                    />
                    <Route path="/flows/:id" exact component={FlowShow} />
                    <Route
                        path="/visualizations"
                        exact
                        component={Visualization}
                    />
                </Switch>
            </div>
        </Router>
    );
};

export default App;
