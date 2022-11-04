/* This example requires Tailwind CSS v2.0+ */
import * as React from 'react';
import { Fragment, useState, useEffect } from 'react';
import { Transition } from '@headlessui/react';
import { XIcon } from '@heroicons/react/outline';
import { getGithubRepos, postMonitoredRepos } from '../api';
import RepoCard from './RepoCard';
import { Repo, MonitoredRepo } from '../types';

interface AddRepoModalProps {
  openCounter: number;
  githubLogoUri: string;
  mrepos: MonitoredRepo[];
}

const AddRepoModal: React.FC<AddRepoModalProps> = ({ mrepos, openCounter, githubLogoUri }: AddRepoModalProps) => {
  const [open, setOpen] = useState(false);
  const [repos, setRepos] = useState(null);
  const [selectedRepos, setSelectedRepos] = useState<Repo[]>([]);

  useEffect(() => {
    openCounter > 0 ? setOpen(!open) : null;
  }, [openCounter]);

  useEffect(() => {
    const token = localStorage.getItem('token') as string;

    if (open) {
      getGithubRepos(token).then((data) => {
        setRepos(data);
      });
    }
  }, [open]);

  const repoSelectHandler = (repository: Repo) => {
    const found = selectedRepos.find((repo) => repo.id === repository.id);

    let newState;

    if (found) {
      newState = selectedRepos.filter((repo) => repo.id !== repository.id);
    }

    if (!found) {
      newState = [...selectedRepos, repository];
    }

    setSelectedRepos(newState);
  };

  // TODO: Implement the handler with API call
  const addRepoSubmitHandler = async (event: React.MouseEvent) => {
    event.preventDefault();

    const token = localStorage.getItem('token');
    await postMonitoredRepos(token, selectedRepos);

    setSelectedRepos([]);
  };

  return (
    <Transition.Root show={open} as={Fragment}>
      <div className="relative z-10">
        <Transition.Child
          as={Fragment}
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div onClick={() => setOpen(false)} className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
        </Transition.Child>
        <div className="fixed flex left-[50%] translate-x-[-50%]">
          <Transition.Child
            as={Fragment}
            enter="ease-out duration-300"
            enterFrom="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
            enterTo="opacity-100 translate-y-0 sm:scale-100"
            leave="ease-in duration-200"
            leaveFrom="opacity-100 translate-y-0 sm:scale-100"
            leaveTo="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
          >
            <div className="relative bg-white dark:bg-dolist-bg-dark rounded px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:max-w-lg sm:w-full sm:p-6">
              <div className="hidden sm:block absolute top-0 right-0 pt-4 pr-4">
                <button
                  type="button"
                  className="bg-white rounded-md text-black dark:text-white focus:outline-none"
                  onClick={() => setOpen(false)}
                >
                  <span className="sr-only">Close</span>
                  <XIcon className="h-6 w-6 bg-white dark:bg-dolist-bg-dark" aria-hidden="true" />
                </button>
              </div>
              <div className="sm:flex sm:flex-col sm:items-start">
                <div className="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
                  <h3 className="text-lg leading-6 font-std font-bold text-black dark:text-white">
                    {`Add Repositories`}
                  </h3>
                </div>
                <span className="w-[95%] ml-4 mt-4 border-b border-dolist-lightgray dark:border-dolist-cream" />
              </div>
              <div className="flex flex-col w-[95%] ml-4 mt-4 min-h-[200px] max-h-[250px] overflow-hidden">
                <div className="flex flex-col w-full overflow-y-scroll">
                  {/** TODO: Add Loader */}
                  {repos
                    ? repos.map((repo, index) => {
                        const repository: Repo = {
                          id: repo.id,
                          name: repo.name,
                          fullName: repo.full_name,
                          defaultBranch: repo.default_branch,
                          language: repo.language,
                          url: repo.url,
                          visibility: repo.visibility,
                          provider: 'github',
                        };

                        const monitored = mrepos.find((mrepo) => mrepo.fullName == repository.fullName);

                        const selected = selectedRepos.find((repo) => repo.id === repository.id);
                        return (
                          <RepoCard
                            key={index}
                            isSelected={selected ? true : false}
                            isMonitored={monitored ? true : false}
                            repository={repository}
                            githubLogoUri={githubLogoUri}
                            selectHandler={repoSelectHandler}
                          />
                        );
                      })
                    : null}
                  {}
                </div>
              </div>
              <div className="mt-5 sm:mt-4 sm:flex sm:flex-row-reverse">
                <button
                  type="button"
                  className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-dolist-darkblue dark:bg-dolist-green text-base font-std font-bold text-white focus:outline-none focus:ring-2 focus:ring-offset-2 sm:ml-3 sm:w-auto sm:text-sm"
                  onClick={async (e) => {
                    await addRepoSubmitHandler(e);
                    setOpen(false);
                  }}
                >
                  Confirm
                </button>
              </div>
            </div>
          </Transition.Child>
        </div>
      </div>
    </Transition.Root>
  );
};

export default AddRepoModal;
