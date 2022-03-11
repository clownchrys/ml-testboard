import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export type ContentState = { page: string }

const name = "menu";
const initialState: ContentState = { page: "/" }

export const { actions, reducer } = createSlice({
  name,
  initialState,
  reducers: {
    setMenu(state, action: PayloadAction<string>) {
      return { page: action.payload };
    },
  }
})
export default reducer;