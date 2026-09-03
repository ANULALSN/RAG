export interface Subject {
  id: number;
  name: string;
  shortName: string;
}

export const subjects: Subject[] = [
  {
    id: 1,
    name: "Big Data",
    shortName: "BD",
  },
  {
    id: 2,
    name: "DBMS",
    shortName: "DB",
  },
  {
    id: 3,
    name: "Computer Networks",
    shortName: "CN",
  },
  {
    id: 4,
    name: "Operating Systems",
    shortName: "OS",
  },
];