import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export type TableState = {
  dataSource: any[],
  isLoading: boolean,
  isSimpleMode: boolean,
  pageSize: number
};

const name = "table";
const initialState: TableState = {
  dataSource: [],
  isLoading: false,
  isSimpleMode: true,
  pageSize: 1000
};

export const { actions, reducer } = createSlice({
  name,
  initialState,
  reducers: {
    resetDataSource(state) {
      return { ...state, dataSource: initialState.dataSource };
    },
    setDataSource(state, { payload }: PayloadAction<TableState["dataSource"]>) {
      return { ...state, dataSource: payload };
    },
    setLoading(state, { payload }: PayloadAction<TableState["isLoading"]>) {
      return { ...state, isLoading: payload };
    },
    setSimpleMode(state, { payload }: PayloadAction<TableState["isSimpleMode"]>) {
      return ({ ...state, isSimpleMode: payload });
    },
    setPageSize(state, { payload }: PayloadAction<TableState["pageSize"]>) {
      return { ...state, pageSize: payload };
    }
  }
})

export default reducer;