import React from 'react';

export interface IGlobalContext {
  theme: 'light' | 'dark' | null;
  switchToLight: () => void;
  switchToDark: () => void;
}

type ObjType = Record<string, unknown>;
type DefaultValue = undefined;
type ContextValue = DefaultValue | IGlobalContext;

export const GlobalContext = React.createContext<ContextValue>(undefined);

export class GlobalContextProvider extends React.Component<ObjType, IGlobalContext> {
  constructor(props: ObjType) {
    super(props);
    this.state = {
      theme: null,
      switchToLight: this.switchToLight.bind(this),
      switchToDark: this.switchToDark.bind(this),
    };
  }

  componentDidMount(): void {
    if (localStorage.theme === 'dark') {
      this.setState({ theme: 'dark' });
    }
    if (localStorage.theme === 'light') {
      this.setState({ theme: 'light' });
    }
  }

  // TODO: Apply transition animation at the switch
  switchToLight() {
    localStorage.theme = 'light';
    document.documentElement.classList.remove('dark');

    this.setState({ theme: 'light' });
  }

  switchToDark() {
    localStorage.theme = 'dark';
    document.documentElement.classList.add('dark');

    this.setState({ theme: 'dark' });
  }

  render(): React.ReactNode {
    return <GlobalContext.Provider value={this.state}>{this.props.children}</GlobalContext.Provider>;
  }
}
