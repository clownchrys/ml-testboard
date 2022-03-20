import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { CSVLink } from "react-csv";
import Highlighter from "react-highlight-words";
import { Button, Form, Input, Space, Switch, Table, TableProps } from 'antd';
import { useForm } from "antd/lib/form/Form";
import { EnterOutlined, DownloadOutlined, SearchOutlined } from "@ant-design/icons";
import { actions as tableActions } from "reducers/table";
import type { FilterDropdownProps } from "antd/lib/table/interface";
import type { ColumnType2, HighlightFilterState } from "types/table";
import type { RootState } from "reducers";


type Props<EntityModel> = {
  columns: ColumnType2<EntityModel>[],
}

function TableComponent<EntityModel extends object>({ columns }: Props<EntityModel>) {
  const { dataSource, isLoading, pageSize, isSimpleMode } = useSelector((state: RootState) => state.table);
  const dispatch = useDispatch();

  // monitoring function
  const onChange: TableProps<EntityModel>["onChange"] = (pagination, filters, sorter, extra) => {
    console.log({ type: "onChange", pagination, filters, sorter, extra })
  };

  // column preference
  columns.forEach((col) => {
    const { dataIndex } = col;
    col.ellipsis = isSimpleMode;
    col.sorter = (a, b) => (a[dataIndex] ?? Number.NEGATIVE_INFINITY) > (b[dataIndex] ?? Number.NEGATIVE_INFINITY) ? 1 : -1
    col.showSorterTooltip = true;
  });

  // custom filter
  const [ highlightFilter, setHighlightFilter ] = useState<HighlightFilterState>({});

  const handleSearch = (selectedKeys: FilterDropdownProps["selectedKeys"], confirm: FilterDropdownProps["confirm"], dataIndex: keyof EntityModel) => {
    confirm({ closeDropdown: true });
    setHighlightFilter({
      searchText: selectedKeys[0] as string,
      searchColumn: dataIndex as string,
    })
  }
  const handleReset = (clearFilters: FilterDropdownProps["clearFilters"], confirm: FilterDropdownProps["confirm"]) => {
    clearFilters?.();
    confirm();
    setHighlightFilter({ ...highlightFilter, searchText: "" })
  }
  const getColumnFilterProps = (dataIndex: keyof EntityModel ): Partial<ColumnType2<EntityModel>> => {
    // filter logic
    const onFilter: ColumnType2<EntityModel>["onFilter"] = ((searchValue, record) => {
      if (!record) {
        return false;
      }
      const _value = String(record[dataIndex]).toLowerCase();
      const _searchValue = String(searchValue).toLowerCase();
      return _value.includes(_searchValue);
    })
    // Visibility callback
    const onFilterDropdownVisibleChange: ColumnType2<EntityModel>["onFilterDropdownVisibleChange"] = ( visible: boolean ) => {}
    // dropdown component
    const filterDropdown: ColumnType2<EntityModel>["filterDropdown"] = ({ setSelectedKeys, selectedKeys, confirm, clearFilters }) => (
      <div style={ { padding: 8 } }>
        <Input
          placeholder={ `Search ${ dataIndex }` }
          value={ selectedKeys[0] }
          onChange={ e => setSelectedKeys(e.target.value ? [ e.target.value ] : []) }
          onPressEnter={ () => handleSearch(selectedKeys, confirm, dataIndex) }
          style={ { marginBottom: 8, display: "block" } }
        />
        <Space>
          <Button
            type="primary" size="small" icon={ <SearchOutlined/> } style={ { width: 90 } }
            onClick={ () => handleSearch(selectedKeys, confirm, dataIndex) }
          >Search</Button>
          <Button
            size="small" style={ { width: 90 } }
            onClick={ () => handleReset(clearFilters, confirm) }
          >Reset</Button>
        </Space>
      </div>
    )
    // row rendering to highlight
    const render: ColumnType2<EntityModel>["render"] = ( text: any ) => {
      const highlightStyle: React.CSSProperties = { backgroundColor: '#ffc069', padding: 0 };
      const searchWords: string[] = [ highlightFilter.searchText ?? "" ];
      const textValue: string = text?.toString() ?? "";

      return (highlightFilter.searchColumn === dataIndex)
        ? <Highlighter highlightStyle={ highlightStyle } searchWords={ searchWords } textToHighlight={ textValue } autoEscape/>
        : (textValue.startsWith("http")) ? <a href={ text } rel="noreferrer" target="_blank">{ text }</a> : text
    }
    return {
      filterDropdown, onFilter, onFilterDropdownVisibleChange, render,
      filterIcon: (filtered) => <SearchOutlined style={ { color: filtered ? '#1890ff' : undefined, fontSize: 15 } }/>,
    }
  };

  // dynamic page size
  const [ form ] = useForm();
  const onFinishPageSizeForm = (values: any) => {
    const msg = `행의 개수를 변경하시겠습니까? (현재: ${ pageSize } -> 변경: ${ values.page_size })`;
    if (values.page_size && confirm(msg)) {
      dispatch(tableActions.setPageSize(values.page_size))
      form.resetFields();
    }
  }

  // actual rendering
  return <div>
    {/* buttons */}
    <div style={{ display: "flex", flexDirection: "row", justifyContent: "space-between" }}>
      {/* left-side */}
      <Space size={ 10 } align="baseline">
        <CSVLink
          data={ dataSource ?? [] }
          headers={ columns.map(value => ({ label: value.title.toString(), key: value.dataIndex.toString() })) }
          filename="csv_exported"
        >
          <Button icon={ <DownloadOutlined/> }>Export CSV</Button>
        </CSVLink>
      </Space>

      {/* right-side */}
      <Form form={ form } onFinish={ onFinishPageSizeForm }>
        <Space size={ 10 } align="baseline">
          <Switch
            checkedChildren="심플 모드"
            unCheckedChildren="심플 모드"
            // onChange={(checked) => setEllipsis(checked)}
            onChange={(isSimpleMode) => dispatch(tableActions.setSimpleMode(isSimpleMode))}
            style={{ marginRight: 10 }}
            defaultChecked={ isSimpleMode }
          />
          <Form.Item name="page_size" rules={[ { pattern: new RegExp(/^[0-9]+$/) } ]}>
            <Input placeholder={ `${ pageSize } 행 / 페이지` }/>
          </Form.Item>
          <Button htmlType="submit" icon={ <EnterOutlined/> }/>
        </Space>
      </Form>
    </div>

    {/* Table */}
    <Table
      dataSource={ dataSource?.map(((value, index) => ({ key: index, ...value }))) }
      columns={ columns?.map((col) => ({ ...col, ...getColumnFilterProps(col.dataIndex) })) as TableProps<EntityModel>["columns"] }
      loading={ { tip: "데이터를 불러오는 중입니다...", spinning: isLoading } }
      size="small"
      pagination={ { pageSize, position: [ "bottomCenter" ], hideOnSinglePage: true } }
      onChange={ onChange }
      title={ (data) => <div style={{ color: "rgb(38, 38, 38)", padding: "px"}}>{ data.length } of { dataSource.length } rows</div> }
      scroll={ { x: "100%", scrollToFirstRowOnChange: true } }
      bordered
      sticky
    />
  </div>
}

export default TableComponent;
