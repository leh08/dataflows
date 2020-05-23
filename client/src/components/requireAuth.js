import React from 'react';
import { connect } from 'react-redux';
import history from '../history';

export default ChildComponent => {
  class ComposedComponent extends React.Component {
    // Our component just got rendered
    componentDidMount() {
      this.shouldNavigateAway();
    }
    // Our component just got updated
    componentDidUpdate() {
      this.shouldNavigateAway();
    }
    shouldNavigateAway() {
      if (!this.props.auth) {
        history.push('/');
      }
    }
    render() {
      return <ChildComponent {...this.props} />;
    }
  }
  function mapStateToProps(state) {
    return { auth: state.auth.isSignedIn };
  }
  return connect(mapStateToProps)(ComposedComponent);
};