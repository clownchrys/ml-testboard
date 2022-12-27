import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export type RenderState = {
  itemType?: string,
  itemIds?: string[],
  currentItemIds?: string[],
  renderUrl?: string,
};

const name = "render";
const initialState: RenderState = {};

export const { actions, reducer } = createSlice({
  name,
  initialState,
  reducers: {
    initState() {
      return { ...initialState }
    },
    setState(currentState, { payload }: PayloadAction<Partial<RenderState>>) {
      return { ...currentState, ...payload }
    },
  }
})

export default reducer;