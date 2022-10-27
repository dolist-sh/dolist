import React from 'react';
import { MonitoredRepo } from '../types';

export interface IGlobalContext {
  theme: 'light' | 'dark' | null;
  monitoredRepos: MonitoredRepo[];
  switchToLight: () => void;
  switchToDark: () => void;
  setMonitoredRepos: (data: MonitoredRepo[]) => void;
  getMonitoredRepo: (fullName: string) => MonitoredRepo;
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
      monitoredRepos: [],
      switchToLight: this.switchToLight.bind(this),
      switchToDark: this.switchToDark.bind(this),
      setMonitoredRepos: this.setMonitoredRepos.bind(this),
      getMonitoredRepo: this.getMonitoredRepo.bind(this),
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

  setMonitoredRepos(data: MonitoredRepo[]) {
    this.setState({ monitoredRepos: data });
  }

  getMonitoredRepo(mrepoId: string): MonitoredRepo | null {
    const result = this.state.monitoredRepos.find((mrepo) => mrepo.id == mrepoId);

    if (!result) return null;

    return result;
  }

  render(): React.ReactNode {
    return <GlobalContext.Provider value={this.state}>{this.props.children}</GlobalContext.Provider>;
  }
}
