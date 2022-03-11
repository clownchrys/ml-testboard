import { ColumnType } from "antd/lib/table";
import { DataIndex } from "rc-table/lib/interface";

export interface ColumnType2<RecordType> extends Omit<ColumnType<RecordType>, "dataIndex"> {
  title: string,
  dataIndex: keyof RecordType,
}

export interface HighlightFilterState {
  searchText?: string,
  searchColumn?: DataIndex
}
