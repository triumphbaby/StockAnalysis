import React, { useState } from 'react';
import { AutoComplete, Input } from 'antd';
import { SearchOutlined } from '@ant-design/icons';
import { get } from '../services/api';
import './StockSearch.css';

interface StockOption {
  value: string;
  label: string;
  stock_code: string;
  name: string;
  industry?: string;
  market?: string;
}

interface StockSearchProps {
  onSelect?: (stockCode: string, stockInfo: any) => void;
  placeholder?: string;
  style?: React.CSSProperties;
}

const StockSearch: React.FC<StockSearchProps> = ({
  onSelect,
  placeholder = "搜索股票代码或名称",
  style
}) => {
  const [options, setOptions] = useState<StockOption[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (searchText: string) => {
    if (!searchText || searchText.length < 1) {
      setOptions([]);
      return;
    }

    setLoading(true);
    try {
      const response = await get(`/api/stocks/search?keyword=${searchText}`);
      const stocks = response.data || [];

      const searchOptions: StockOption[] = stocks.map((stock: any) => ({
        value: stock.stock_code,
        label: `${stock.name} (${stock.stock_code})`,
        stock_code: stock.stock_code,
        name: stock.name,
        industry: stock.industry,
        market: stock.market
      }));

      setOptions(searchOptions);
    } catch (error) {
      console.error('搜索股票失败:', error);
      setOptions([]);
    } finally {
      setLoading(false);
    }
  };

  const handleSelect = (value: string) => {
    if (onSelect) {
      const selectedOption = options.find(opt => opt.value === value);
      if (selectedOption) {
        onSelect(selectedOption.stock_code, selectedOption);
      }
    }
  };

  return (
    <div className="stock-search-container" style={style}>
      <AutoComplete
        options={options}
        onSearch={handleSearch}
        onSelect={handleSelect}
        style={{ width: '100%' }}
        notFoundContent={
          loading ? (
            <div className="stock-search-loading">
              <span>🔍 搜索中...</span>
            </div>
          ) : (
            <div className="stock-search-empty">
              <span>😕 无匹配结果</span>
            </div>
          )
        }
        popupClassName="stock-search-dropdown"
        filterOption={false}
      >
        <Input
          size="large"
          prefix={<SearchOutlined />}
          placeholder={placeholder}
          allowClear
        />
      </AutoComplete>
    </div>
  );
};

export default StockSearch;
