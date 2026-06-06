
import {Fragment,memo,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {EventLoopContext,StateContexts} from "$/utils/context"
import {Badge as RadixThemesBadge,Button as RadixThemesButton,Flex as RadixThemesFlex,Table as RadixThemesTable} from "@radix-ui/themes"
import {jsx} from "@emotion/react"






export const Foreach_comp_e771b2455fa5690348265f7f9ff3607e = memo(({children}) => {
    const reflex___state____state__sandbox_reflex___state_hoteis____hotel_state = useContext(StateContexts.reflex___state____state__sandbox_reflex___state_hoteis____hotel_state)
const [addEvents, connectErrors] = useContext(EventLoopContext);



    return(
        Array.prototype.map.call(reflex___state____state__sandbox_reflex___state_hoteis____hotel_state.solicitacoes_rx_state_ ?? [],((req_rx_state_,index_cec8012ea84eaf39ea7eb070a24ac600)=>(jsx(RadixThemesTable.Row,{key:index_cec8012ea84eaf39ea7eb070a24ac600},jsx(RadixThemesTable.Cell,{},jsx(RadixThemesBadge,{color:((req_rx_state_?.["tipo"]?.valueOf?.() === "EDIT"?.valueOf?.()) ? "yellow" : "red")},req_rx_state_?.["tipo"])),jsx(RadixThemesTable.Cell,{},req_rx_state_?.["rid"]),jsx(RadixThemesTable.Cell,{},req_rx_state_?.["nome"]),jsx(RadixThemesTable.Cell,{},jsx(RadixThemesFlex,{align:"start",className:"rx-Stack",direction:"row",gap:"2"},jsx(RadixThemesButton,{css:({ ["cursor"] : "pointer", ["color"] : "green" }),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state_hoteis____hotel_state.approve_solicitacao", ({ ["req_id"] : req_rx_state_?.["id"] }), ({  })))], [_e], ({  })))),variant:"ghost"},"\u2705"),jsx(RadixThemesButton,{css:({ ["cursor"] : "pointer", ["color"] : "red" }),onClick:((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state_hoteis____hotel_state.reject_solicitacao", ({ ["req_id"] : req_rx_state_?.["id"] }), ({  })))], [_e], ({  })))),variant:"ghost"},"\u274c")))))))
    )
});
